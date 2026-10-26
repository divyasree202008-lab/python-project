
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pandu@20062008",
    database="movie_recommendation"
)

print("Database connected successfully!")

try:
    # Step 2: Fetch movie ratings
    query = """
    SELECT
        m.movie_id,
        m.title,
        m.genre,
        ROUND(AVG(r.rating), 2) AS average_rating,
        COUNT(r.rating) AS rating_count
    FROM movies m
    LEFT JOIN ratings r
        ON m.movie_id = r.movie_id
    GROUP BY m.movie_id, m.title, m.genre
    """

    df = pd.read_sql(query, conn)

    # Step 3: Display movies that have ratings
    rated_movies = df[df["rating_count"] > 0].copy()

    rated_movies = rated_movies.sort_values(
        by=["average_rating", "rating_count"],
        ascending=[False, False]
    )

    print("\n===== MOVIE RATINGS ANALYSIS =====")

    if not rated_movies.empty:
        print(rated_movies.to_string(index=False))

        # Step 4: NumPy statistical analysis
        ratings = rated_movies["average_rating"].dropna().to_numpy()

        if len(ratings) > 0:
            print("\n===== NUMPY RATING STATISTICS =====")
            print("Mean rating:", round(np.mean(ratings), 2))
            print("Median rating:", round(np.median(ratings), 2))
            print("Highest average rating:", round(np.max(ratings), 2))
            print("Lowest average rating:", round(np.min(ratings), 2))
    else:
        print("No movies have ratings yet.")

    # Step 5: Display top 10 movies
    top_movies = rated_movies[
        rated_movies["rating_count"] >= 2
    ].head(10)

    print("\n===== TOP-RATED MOVIES =====")

    if not top_movies.empty:
        print(
            top_movies[
                ["title", "genre", "average_rating", "rating_count"]
            ].to_string(index=False)
        )

        # Step 6: Chart for top-rated movies
        plt.figure(figsize=(10, 6))

        plt.barh(
            top_movies["title"],
            top_movies["average_rating"]
        )

        plt.xlabel("Average Rating")
        plt.ylabel("Movie")
        plt.title("Top 10 Telugu Movies by Rating")
        plt.xlim(0, 5)
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

    else:
        print("No movies have at least 2 ratings.")

    # Step 7: Genre analysis
    genre_query = """
    SELECT
        m.genre,
        ROUND(AVG(r.rating), 2) AS average_rating,
        COUNT(r.rating) AS total_ratings
    FROM movies m
    LEFT JOIN ratings r
        ON m.movie_id = r.movie_id
    GROUP BY m.genre
    ORDER BY average_rating DESC
    """

    genre_df = pd.read_sql(genre_query, conn)

    print("\n===== GENRE ANALYSIS =====")
    print(genre_df.to_string(index=False))

    # Step 8: Chart for average rating by genre
    rated_genres = genre_df.dropna(
        subset=["average_rating"]
    )

    if not rated_genres.empty:
        plt.figure(figsize=(9, 5))

        plt.bar(
            rated_genres["genre"],
            rated_genres["average_rating"]
        )

        plt.xlabel("Genre")
        plt.ylabel("Average Rating")
        plt.title("Average Rating by Genre")
        plt.ylim(0, 5)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No genre ratings available for plotting.")

    print("\nAnalysis completed successfully!")

finally:
    # Step 9: Close database connection
    conn.close()
    print("Database connection closed.")



