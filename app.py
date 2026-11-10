
import re
import os

from dotenv import load_dotenv
from flask import (
    Flask, request, render_template, redirect,
    url_for, flash, session
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY is missing from your .env file.")


# ---------------- DATABASE CONNECTION ----------------

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        use_pure=True
    )


# ---------------- GET MOVIES ----------------

def get_movies(search_query="", selected_genre="", selected_year="", min_rating=""):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            COALESCE(AVG(r.rating), 0) AS avg_rating,
            COUNT(r.rating_id) AS rating_count
        FROM movies m
        LEFT JOIN ratings r ON m.movie_id = r.movie_id
        WHERE 1=1
    """

    params = []

    if search_query:
        sql += " AND (m.title LIKE %s OR m.genre LIKE %s)"
        search_value = "%" + search_query + "%"
        params.extend([search_value, search_value])

    if selected_genre:
        sql += " AND FIND_IN_SET(%s, REPLACE(m.genre, ', ', ',')) > 0"
        params.append(selected_genre)

    if selected_year:
        sql += " AND m.release_year = %s"
        params.append(int(selected_year))

    sql += """
        GROUP BY
            m.movie_id, m.title, m.release_year,
            m.genre, m.poster_url
    """

    if min_rating:
        sql += " HAVING COALESCE(AVG(r.rating), 0) >= %s"
        params.append(float(min_rating))

    sql += " ORDER BY m.title"

    cursor.execute(sql, tuple(params))
    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return movies


# ---------------- GET FAVORITE GENRES ----------------

def get_favorite_genres(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT genre FROM user_genres WHERE user_id = %s ORDER BY genre",
        (user_id,)
    )

    genres = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return genres


# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("landing.html")

    # Keep your existing movie dashboard code below

    search_query = request.args.get("search", "").strip()
    selected_genre = request.args.get("genre", "").strip()
    selected_year = request.args.get("year", "").strip()
    min_rating = request.args.get("min_rating", "").strip()

    movies = get_movies(
        search_query,
        selected_genre,
        selected_year,
        min_rating
    )

    user_id = session["user_id"]

    favorite_genres = get_favorite_genres(user_id)
    recommendations = []
    top_movies = []

    # ---------------- PERSONALIZED RECOMMENDATIONS ----------------

        
        if favorite_genres:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Match movies with any of the user's favorite genres
            genre_conditions = " OR ".join(
                ["FIND_IN_SET(%s, REPLACE(m.genre, ', ', ',')) > 0"]
                * len(favorite_genres)
            )

            recommendation_sql = f"""
                SELECT
                    m.movie_id,
                    m.title,
                    m.release_year,
                    m.genre,
                    m.poster_url,
                    AVG(r.rating) AS avg_rating,
                    COUNT(r.rating_id) AS rating_count
                FROM movies m
                LEFT JOIN ratings r
                    ON m.movie_id = r.movie_id
                WHERE ({genre_conditions})
                  AND NOT EXISTS (
                      SELECT 1
                      FROM ratings ur
                      WHERE ur.movie_id = m.movie_id
                        AND ur.user_id = %s
                  )
                GROUP BY
                    m.movie_id,
                    m.title,
                    m.release_year,
                    m.genre,
                    m.poster_url
                ORDER BY
                    avg_rating DESC,
                    rating_count DESC,
                    m.title
                LIMIT 10
            """

        parameters = tuple(favorite_genres) + (user_id,)

        cursor.execute(recommendation_sql, parameters)
        recommendations = cursor.fetchall()

        # Explain why each movie is recommended
        for movie in recommendations:
            movie_genres = [
                genre.strip()
                for genre in movie["genre"].split(",")
            ] if movie["genre"] else []

            matching_genres = [
                genre for genre in favorite_genres
                if genre in movie_genres
            ]

            if matching_genres:
                movie["recommendation_reason"] = (
                    "Recommended because you like: "
                    + ", ".join(matching_genres)
                )
            else:
                movie["recommendation_reason"] = (
                    "Recommended based on your favorite genres."
                )

        cursor.close()
        conn.close()

    # ---------------- TOP FIVE MOVIES ----------------


    # Get top five movies that have at least one rating
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            AVG(r.rating) AS avg_rating,
            COUNT(r.rating_id) AS rating_count
        FROM movies m
        INNER JOIN ratings r ON m.movie_id = r.movie_id
        GROUP BY
            m.movie_id, m.title, m.release_year,
            m.genre, m.poster_url
        ORDER BY avg_rating DESC, rating_count DESC, m.title
        LIMIT 5
    """)

    top_movies = cursor.fetchall()

    cursor.close()
    conn.close()

    genres = [
        "Action", "Comedy", "Drama", "Fantasy", "Horror",
        "Mystery", "Romance", "Sci-Fi", "Thriller"
    ]

    return render_template(
        "index.html",
        movies=movies,
        recommendations=recommendations,
        favorite_genres=favorite_genres,
        search_query=search_query,
        top_movies=top_movies,
        genres=genres,
        selected_genre=selected_genre,
        selected_year=selected_year,
        min_rating=min_rating
    )


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not display_name or not email or not username or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        if not re.fullmatch(
            r"(?=.*[A-Za-z])(?=.*[0-9])[A-Za-z0-9]+",
            username
        ):
            flash(
                "Username must contain letters and numbers only.",
                "error"
            )
            return redirect(url_for("register"))

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Check username
            cursor.execute(
                "SELECT user_id FROM users WHERE username = %s",
                (username,)
            )

            if cursor.fetchone():
                flash(
                    "Username already exists. Please choose another.",
                    "error"
                )
                return redirect(url_for("register"))

            # Check email
            cursor.execute(
                "SELECT user_id FROM users WHERE email = %s",
                (email,)
            )

            if cursor.fetchone():
                flash(
                    "Email already registered. Please use another email.",
                    "error"
                )
                return redirect(url_for("register"))

            # Hash password
            password_hash = generate_password_hash(password)

            cursor.execute("""
                INSERT INTO users
                    (display_name, email, username, password_hash)
                VALUES (%s, %s, %s, %s)
            """, (display_name, email, username, password_hash))

            conn.commit()

            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))

        except Exception:
            conn.rollback()
            flash(
                "Registration failed. Please check your details and try again.",
                "error"
            )
            app.logger.exception("Registration failed")

        finally:
            cursor.close()
            conn.close()

    return render_template("auth.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Check empty fields
        if not username or not password:
            flash("Please enter username and password.", "error")
            return redirect(url_for("login"))

        conn = None
        cursor = None

        try:
            # Connect to MySQL
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Find user in database
            cursor.execute("""
                SELECT user_id, display_name, username, password_hash
                FROM users
                WHERE username = %s
            """, (username,))

            user = cursor.fetchone()

            # Check whether user exists
            print("User found:", bool(user))

            # Check password
            password_ok = False

            if user:
                password_ok = check_password_hash(
                    user["password_hash"], password
                )

            print("Password correct:", password_ok)

            # Successful login
            if user and password_ok:

                session.clear()

                session["user_id"] = user["user_id"]
                session["display_name"] = user["display_name"]

                flash("Welcome to CineMatch!", "success")

                return redirect(url_for("index"))

            else:
                flash("Invalid username or password.", "error")
                return redirect(url_for("login"))

        except Exception as e:
            print("Login error:", e)
            flash("Something went wrong. Please try again.", "error")
            return redirect(url_for("login"))

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return render_template("auth.html", mode="login")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


# ---------------- SAVE FAVORITE GENRES ----------------

# ---------------- SAVE FAVORITE GENRES ----------------

@app.route("/save_genres", methods=["GET", "POST"])
def save_genres():

    if not session.get("user_id"):
        flash("Please log in to select your favorite genres.", "error")
        return redirect(url_for("login"))

    valid_genres = [
        "Action", "Comedy", "Drama", "Fantasy", "Horror",
        "Mystery", "Romance", "Sci-Fi", "Thriller"
    ]

    # Display the genre selection page
    if request.method == "GET":
        return render_template("genres.html", genres=valid_genres)

    # Save selected genres
    user_id = session["user_id"]
    selected_genres = request.form.getlist("genres")

    selected_genres = [
        genre for genre in selected_genres
        if genre in valid_genres
    ]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM user_genres WHERE user_id = %s",
            (user_id,)
        )

        for genre in selected_genres:
            cursor.execute("""
                INSERT INTO user_genres (user_id, genre)
                VALUES (%s, %s)
            """, (user_id, genre))

        conn.commit()
        flash("Your favorite genres have been saved!", "success")

    except Exception:
        conn.rollback()
        app.logger.exception("Saving genres failed")
        flash("Unable to save genres.", "error")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("index"))



# ---------------- RATE A MOVIE ----------------

@app.route("/rate", methods=["POST"])
def rate_movie():

    if not session.get("user_id"):
        flash("Please log in to rate movies.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    try:
        movie_id = int(request.form.get("movie_id", ""))
        rating = float(request.form.get("rating", ""))

        if not 1 <= rating <= 5:
            flash("Rating must be between 1 and 5.", "error")
            return redirect(request.referrer or url_for("index"))

    except (ValueError, TypeError):
        flash("Please select a valid movie and rating.", "error")
        return redirect(request.referrer or url_for("index"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT movie_id FROM movies WHERE movie_id = %s",
        (movie_id,)
    )

    movie = cursor.fetchone()

    if not movie:
        cursor.close()
        conn.close()

        flash("Movie not found.", "error")
        return redirect(url_for("index"))

    cursor.execute("""
        INSERT INTO ratings (user_id, movie_id, rating)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            rating = VALUES(rating),
            rated_at = CURRENT_TIMESTAMP
    """, (user_id, movie_id, rating))

    conn.commit()

    cursor.close()
    conn.close()

    session.pop("_flashes", None)

    flash("Your rating has been saved!", "success")
    return redirect(request.referrer or url_for("index"))


# ---------------- MOVIE DETAILS ----------------

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):

    if not session.get("user_id"):
        flash("Please log in to view movies.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get selected movie details
    cursor.execute("""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            COALESCE(AVG(r.rating), 0) AS avg_rating,
            COUNT(r.rating_id) AS rating_count
        FROM movies m
        LEFT JOIN ratings r ON m.movie_id = r.movie_id
        WHERE m.movie_id = %s
        GROUP BY
            m.movie_id, m.title, m.release_year,
            m.genre, m.poster_url
    """, (movie_id,))

    movie = cursor.fetchone()

    if not movie:
        cursor.close()
        conn.close()

        flash("Movie not found.", "error")
        return redirect(url_for("index"))

    # Get similar movies from the same genre
    cursor.execute("""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            COALESCE(AVG(r.rating), 0) AS avg_rating,
            COUNT(r.rating_id) AS rating_count
        FROM movies m
        LEFT JOIN ratings r ON m.movie_id = r.movie_id
        WHERE m.movie_id != %s
          AND m.genre = %s
        GROUP BY
            m.movie_id, m.title, m.release_year,
            m.genre, m.poster_url
        ORDER BY avg_rating DESC, m.title
        LIMIT 6
    """, (movie_id, movie["genre"]))

    similar_movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "movie_details.html",
        movie=movie,
        similar_movies=similar_movies
    )


# ---------------- ADD TO WATCHLIST ----------------

@app.route("/watchlist/add/<int:movie_id>", methods=["POST"])
def add_to_watchlist(movie_id):

    if not session.get("user_id"):
        flash("Please log in to add movies to your watchlist.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT movie_id FROM movies WHERE movie_id = %s",
        (movie_id,)
    )

    movie = cursor.fetchone()

    if not movie:
        cursor.close()
        conn.close()

        flash("Movie not found.", "error")
        return redirect(url_for("index"))

    cursor.execute("""
        INSERT IGNORE INTO watchlist (user_id, movie_id)
        VALUES (%s, %s)
    """, (user_id, movie_id))

    added = cursor.rowcount > 0

    conn.commit()

    cursor.close()
    conn.close()

    if added:
        flash("Movie added to your watchlist!", "success")
    else:
        flash("This movie is already in your watchlist.", "error")

    return redirect(request.referrer or url_for("index"))


# ---------------- VIEW WATCHLIST ----------------

@app.route("/watchlist")
def view_watchlist():

    if not session.get("user_id"):
        flash("Please log in to view your watchlist.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            w.added_at
        FROM watchlist w
        JOIN movies m ON w.movie_id = m.movie_id
        WHERE w.user_id = %s
        ORDER BY w.added_at DESC
    """, (user_id,))

    movies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("watchlist.html", movies=movies)


# ---------------- REMOVE FROM WATCHLIST ----------------

@app.route("/watchlist/remove/<int:movie_id>", methods=["POST"])
def remove_from_watchlist(movie_id):

    if not session.get("user_id"):
        flash("Please log in to manage your watchlist.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM watchlist
        WHERE user_id = %s AND movie_id = %s
    """, (user_id, movie_id))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Movie removed from your watchlist.", "success")
    return redirect(request.referrer or url_for("view_watchlist"))

#-------------------RATING HISTORY---------------------

# ---------------- RATING HISTORY ----------------

@app.route("/rating-history")
def rating_history():

    if "user_id" not in session:
        flash("Please login to view your rating history.", "error")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            m.movie_id,
            m.title,
            m.release_year,
            m.genre,
            m.poster_url,
            r.rating,
            r.rated_at 
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        WHERE r.user_id = %s
        ORDER BY r.rated_at DESC
    """, (session["user_id"],))

    ratings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("rating_history.html", ratings=ratings)


# ---------------- PASSWORD RESET SERIALIZER ----------------

def get_reset_serializer():
    return URLSafeTimedSerializer(app.secret_key)

#---------------------FORGOT PASSWORD------------------------

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    print("FORGOT PASSWORD ROUTE REACHED", flush=True)

    if request.method == "POST":
        print("POST REQUEST RECEIVED", flush=True)

        email = request.form.get("email", "").strip().lower()
        print("EMAIL:", email, flush=True)

        conn = None
        cursor = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT user_id FROM users WHERE email = %s",
                (email,)
            )

            user = cursor.fetchone()

            if user:
                token = get_reset_serializer().dumps(
                    email,
                    salt="password-reset-salt"
                )

                reset_url = url_for(
                    "reset_password",
                    token=token,
                    _external=True
                )

                print("\nYOUR PASSWORD RESET LINK:", flush=True)
                print(reset_url, flush=True)

            else:
                print("EMAIL NOT FOUND IN DATABASE", flush=True)

        except Exception as e:
            print("ERROR:", str(e), flush=True)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return "Check your VS Code terminal for the reset link."

    return render_template("forgot_password.html")
# ---------------- RESET PASSWORD ----------------
@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = get_reset_serializer().loads(
            token,
            salt="password-reset-salt",
            max_age=900
        )
    except SignatureExpired:
        return "Reset link expired. Please request a new link."
    except BadSignature:
        return "Invalid reset link."

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if len(new_password) < 8:
            flash("Password must contain at least 8 characters.")
            return render_template("reset_password.html", token=token)

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return render_template("reset_password.html", token=token)

        hashed_password = generate_password_hash(new_password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = %s WHERE email = %s",
            (hashed_password, email)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Password reset successful!")
        return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)


# ---------------- POSTER PATH COMPATIBILITY ----------------

@app.route("/static/posters/<path:filename>")
def static_posters_redirect(filename):
    return redirect(url_for("static", filename=f"poster/{filename}"))


@app.route("/test-landing")
def test_landing():
    return "CINEMATCH TEST ROUTE IS WORKING"

print(app.url_map)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
