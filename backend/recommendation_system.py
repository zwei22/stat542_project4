import pandas as pd
import json


def most_popular(genre, rating_merged, movies):
    genre_ratings = rating_merged[rating_merged["Genres"].str.contains(genre)]
    id = genre_ratings.groupby("MovieID").size().sort_values(ascending=False)[:10]
    return movies[movies["MovieID"].isin(id.index)][["MovieID", "Title"]]


def get_genre_recommendations(genre):
    with open("genre_recommendations.json") as json_file:
        data = json.load(json_file)
        return data[genre]

    movies = pd.read_csv(
        "movies.dat", sep="::", engine="python", encoding="ISO-8859-1", header=None
    )
    movies.columns = ["MovieID", "Title", "Genres"]
    ratings = pd.read_csv("ratings.dat", sep="::", engine="python", header=None)
    ratings.columns = ["UserID", "MovieID", "Rating", "Timestamp"]
    rating_merged = ratings.merge(movies, left_on="MovieID", right_on="MovieID")
    result = most_popular(genre, rating_merged, movies)

    return result.to_dict("records")

    return [
        {
            "MovieID": "1",
            "Title": "Movie 1",
        },
        {
            "MovieID": "2",
            "Title": "Movie 2",
        },
        {
            "MovieID": "3",
            "Title": "Movie 3",
        },
        {
            "MovieID": "4",
            "Title": "Movie 4",
        },
        {
            "MovieID": "5",
            "Title": "Movie 5",
        },
    ]


def get_collaborative_recommendations(user_ratings):
    # Placeholder function to simulate recommendation logic
    print(user_ratings)
    return [
        {
            "MovieID": "1",
            "Title": "Movie 1",
        },
        {
            "MovieID": "2",
            "Title": "Movie 2",
        },
        {
            "MovieID": "3",
            "Title": "Movie 3",
        },
        {
            "MovieID": "4",
            "Title": "Movie 4",
        },
        {
            "MovieID": "5",
            "Title": "Movie 5",
        },
        {
            "MovieID": "6",
            "Title": "Movie 6",
        },
    ]


if __name__ == "__main__":
    print(get_genre_recommendations("Action"))
