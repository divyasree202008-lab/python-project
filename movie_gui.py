import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pandu@20062008",
        database="movie_recommendation"
    )


def show_movies():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT movie_id, title, genre FROM movies ORDER BY title"
        )
        movies = cursor.fetchall()

        movie_list.delete(*movie_list.get_children())

        for movie in movies:
            movie_list.insert("", "end", values=movie)

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))


def show_recommendations():
    try:
        user_id = int(user_entry.get())

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone() is None:
            messagebox.showerror("Error", "User ID not found.")
            cursor.close()
            conn.close()
            return

        cursor.execute(
            "SELECT genre FROM user_genres WHERE user_id = %s",
            (user_id,)
        )
        genres = [row[0] for row in cursor.fetchall()]

        if not genres:
            messagebox.showinfo(
                "No Favorite Genres",
                "This user has no favorite genres."
            )
            cursor.close()
            conn.close()
            return

        placeholders = ", ".join(["%s"] * len(genres))

        query = f"""
            SELECT m.title, m.genre,
                   ROUND(AVG(r.rating), 2),
                   COUNT(r.rating)
            FROM movies m
            LEFT JOIN ratings r ON m.movie_id = r.movie_id
            WHERE m.genre IN ({placeholders})
              AND m.movie_id NOT IN (
                  SELECT movie_id
                  FROM ratings
                  WHERE user_id = %s
              )
            GROUP BY m.movie_id, m.title, m.genre
            ORDER BY AVG(r.rating) DESC, COUNT(r.rating) DESC
            LIMIT 10
        """

        cursor.execute(query, tuple(genres) + (user_id,))
        results = cursor.fetchall()

        movie_list.delete(*movie_list.get_children())

        for title, genre, avg_rating, count in results:
            rating_text = (
                f"{avg_rating} ({count} ratings)"
                if avg_rating is not None
                else "Not rated yet"
            )
            movie_list.insert(
                "", "end",
                values=("-", title, f"{genre} | {rating_text}")
            )

        if not results:
            messagebox.showinfo(
                "Recommendations",
                "No new movies found for your favorite genres."
            )

        cursor.close()
        conn.close()

    except ValueError:
        messagebox.showerror("Input Error", "Enter a valid numeric user ID.")

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

def submit_rating():
    try:
        user_id = int(user_entry.get())
        movie_id = int(movie_id_entry.get())
        rating = float(rating_entry.get())

        if rating < 1 or rating > 5:
            messagebox.showerror(
                "Invalid Rating",
                "Rating must be between 1 and 5."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        # Check whether the user exists
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = %s",
            (user_id,)
        )

        if cursor.fetchone() is None:
            messagebox.showerror("Error", "User ID not found.")
            cursor.close()
            conn.close()
            return

        # Check whether the movie exists
        cursor.execute(
            "SELECT title FROM movies WHERE movie_id = %s",
            (movie_id,)
        )

        movie = cursor.fetchone()

        if movie is None:
            messagebox.showerror("Error", "Movie ID not found.")
            cursor.close()
            conn.close()
            return

        # Save or update the rating
        cursor.execute(
            """
            INSERT INTO ratings (user_id, movie_id, rating)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            rating = VALUES(rating),
            rated_at = CURRENT_TIMESTAMP
            """,
            (user_id, movie_id, rating)
        )

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Rating saved!\nMovie: {movie[0]}\nRating: {rating}"
        )

        cursor.close()
        conn.close()

    except ValueError:
        messagebox.showerror(
            "Input Error",
            "Enter a valid user ID, movie ID, and rating."
        )

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))
# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("750x500")

heading = tk.Label(
    root,
    text="Movie Recommendation System",
    font=("Arial", 18, "bold")
)
heading.pack(pady=15)

user_frame = tk.Frame(root)
user_frame.pack(pady=5)

tk.Label(user_frame, text="Enter User ID:").pack(side="left", padx=5)

user_entry = tk.Entry(user_frame, width=15)
user_entry.pack(side="left", padx=5)

tk.Button(
    user_frame,
    text="Recommend Movies",
    command=show_recommendations
).pack(side="left", padx=5)

tk.Button(
    root,
    text="Show All Movies",
    command=show_movies
).pack(pady=8)
rating_frame = tk.Frame(root)
rating_frame.pack(pady=5)

tk.Label(rating_frame, text="Movie ID:").pack(side="left", padx=5)

movie_id_entry = tk.Entry(rating_frame, width=8)
movie_id_entry.pack(side="left", padx=5)

tk.Label(rating_frame, text="Rating (1-5):").pack(side="left", padx=5)

rating_entry = tk.Entry(rating_frame, width=8)
rating_entry.pack(side="left", padx=5)

tk.Button(
    rating_frame,
    text="Submit Rating",
    command=submit_rating
).pack(side="left", padx=5)
columns = ("ID", "Title", "Genre / Rating")
movie_list = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=15
)

for col in columns:
    movie_list.heading(col, text=col)

movie_list.column("ID", width=60, anchor="center")
movie_list.column("Title", width=300)
movie_list.column("Genre / Rating", width=300)

movie_list.pack(fill="both", expand=True, padx=15, pady=10)

root.mainloop()