from flask import Flask, jsonify, request, session
from flask_cors import CORS
import pandas as pd

from recommendation_system import (
    get_genre_recommendations,
    get_collaborative_recommendations,
)

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
app.secret_key = "your_secret_key"  # Replace with a real secret key

movies = pd.read_csv(
    "movies.dat", sep="::", engine="python", encoding="ISO-8859-1", header=None
)
movies.columns = ["MovieID", "Title", "Genres"]


genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children's",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
]


@app.route("/api/genres", methods=["GET"])
def list_genres():
    return jsonify(genres)


@app.route("/api/movies", methods=["GET"])
def list_movies():
    movies_head = movies.copy()
    movies_head.drop("Genres", axis=1, inplace=True)
    # Convert to a list of dictionaries
    movies_head = movies_head.head(20).to_dict("records")
    return jsonify(movies_head)


@app.route("/api/rate", methods=["POST"])
def rate_movie():
    data = request.json
    movie_id = data["movie_id"]
    rating = data["rating"]
    return jsonify({"movie_id": movie_id, "rating": rating})


@app.route("/api/recommend/genre", methods=["POST"])
def recommend_by_genre():
    genre = request.json["genre"]
    recommendations = get_genre_recommendations(genre)
    return jsonify(recommendations)


# [
#       {
#         "MovieID": 2,
#         “Title”: “hello”,
#         "Rate": 1,
#       },
#       {
#         "MovieID": 2,
#         “Title”: “hello”,
#         "Rate": 1,
#       },
# ]


@app.route("/api/recommend/collaborative", methods=["POST"])
def recommend_by_collaborative():
    # In a real application, you'd use the user's session or identify them some other way

    user_ratings = request.json
    recommendations = get_collaborative_recommendations(user_ratings)
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7122)
