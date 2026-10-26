import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pandu@20062008",
    database="movie_recommendation"
)

try:
    cursor = conn.cursor()

    user_id = int(input("Enter your user ID: "))

    # Check if the user exists
    cursor.execute(
        "SELECT display_name FROM users WHERE user_id = %s",
        (user_id,)
    )
    user = cursor.fetchone()

    if user is None:
        print("User ID not found.")

    else:
        print("\n===== MY MOVIE RATINGS =====")
        print("User:", user[0])

        cursor.execute(
            """
            SELECT m.title, m.genre, r.rating
            FROM ratings r
            JOIN movies m ON r.movie_id = m.movie_id
            WHERE r.user_id = %s
            ORDER BY m.title
            """,
            (user_id,)
        )

        ratings = cursor.fetchall()

        if not ratings:
            print("You haven't rated any movies yet.")

        else:
            total = 0

            for title, genre, rating in ratings:
                print(
                    f"Movie: {title} | Genre: {genre} | Rating: {rating}"
                )
                total += float(rating)

            average = total / len(ratings)

            print("\nTotal movies rated:", len(ratings))
            print("Your average rating:", round(average, 2))

finally:
    conn.close()
    print("\nDatabase connection closed.")