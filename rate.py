import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pandu@20062008",
    database="movie_recommendation"
)

try:
    cursor = conn.cursor()

    print("===== RATE A MOVIE =====")

    user_id = int(input("Enter your user ID: "))

    # Check whether the user exists
    cursor.execute(
        "SELECT display_name FROM users WHERE user_id = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        print("User ID not found.")

    else:
        print("\nWelcome,", user[0])

        # Display available movies
        cursor.execute(
            "SELECT movie_id, title FROM movies ORDER BY movie_id"
        )

        movies = cursor.fetchall()

        print("\nAvailable Movies:")

        for movie_id, title in movies:
            print(movie_id, "-", title)

        movie_id = int(input("\nEnter the movie ID: "))
        rating = float(input("Enter your rating (1 to 5): "))

        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")

        else:
            # Check whether the movie exists
            cursor.execute(
                "SELECT title FROM movies WHERE movie_id = %s",
                (movie_id,)
            )

            movie = cursor.fetchone()

            if movie is None:
                print("Movie ID not found.")

            else:
                # Insert or update the rating
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

                print("\nRating saved successfully!")
                print("Movie:", movie[0])
                print("Your rating:", rating)

finally:
    conn.close()
    print("\nDatabase connection closed.")