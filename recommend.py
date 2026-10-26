import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pandu@20062008",
    database="movie_recommendation"
)

try:
    user_id = int(input("Enter your user ID: "))

    # Check whether the user exists
    user_query = """
    SELECT user_id, display_name
    FROM users
    WHERE user_id = %s
    """

    user_df = pd.read_sql(user_query, conn, params=(user_id,))

    if user_df.empty:
        print("User ID not found.")

    else:
        print("\nWelcome,", user_df.iloc[0]["display_name"])

        # Get the user's favorite genres
        genre_query = """
        SELECT genre
        FROM user_genres
        WHERE user_id = %s
        """

        genre_df = pd.read_sql(
            genre_query, conn, params=(user_id,)
        )

        if genre_df.empty:
            print("No favorite genres found for this user.")

        else:
            genres = genre_df["genre"].tolist()

            # Recommend movies the user has not rated
            # and that match their favorite genres
            placeholders = ", ".join(["%s"] * len(genres))

            movie_query = f"""
            SELECT
                m.movie_id,
                m.title,
                m.genre,
                ROUND(AVG(r.rating), 2) AS average_rating,
                COUNT(r.rating) AS rating_count
            FROM movies m
            LEFT JOIN ratings r
                ON m.movie_id = r.movie_id
            WHERE m.genre IN ({placeholders})
              AND m.movie_id NOT IN (
                  SELECT movie_id
                  FROM ratings
                  WHERE user_id = %s
              )
            GROUP BY m.movie_id, m.title, m.genre
            ORDER BY
                (AVG(r.rating) IS NULL) ASC,
                AVG(r.rating) DESC,
                COUNT(r.rating) DESC
            LIMIT 10
            """

            params = tuple(genres) + (user_id,)

            recommendations = pd.read_sql(
                movie_query, conn, params=params
            )

            print("\nYour Favorite Genres:", ", ".join(genres))
            print("\n===== RECOMMENDED MOVIES =====")

            if recommendations.empty:
                print("No new movies found for your favorite genres.")

            else:
                recommendations["average_rating"] = (
                    recommendations["average_rating"].fillna(0)
                )

                print(
                    recommendations[
                        ["title", "genre", "average_rating", "rating_count"]
                    ].to_string(index=False)
                )

finally:
    conn.close()
    print("\nDatabase connection closed.")
    # Display a chart of recommended movies
if not recommendations.empty:
    rated = recommendations[
        recommendations["rating_count"] > 0
    ]

    if not rated.empty:
        plt.figure(figsize=(9, 5))

        plt.barh(
            rated["title"],
            rated["average_rating"]
        )

        plt.xlabel("Average Rating")
        plt.ylabel("Movie")
        plt.title("Recommended Movies for You")
        plt.xlim(0, 5)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig("recommended_movies.png")
plt.close()
print("Chart saved as recommended_movies.png")