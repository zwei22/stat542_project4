import pandas as pd
import numpy as np
import json


def most_popular(genre, rating_merged, movies):
    genre_ratings = rating_merged[rating_merged["Genres"].str.contains(genre)]
    id = genre_ratings.groupby("MovieID").size().sort_values(ascending=False)[:10]
    return movies[movies["MovieID"].isin(id.index)][["MovieID", "Title"]]


def get_genre_recommendations(genre):
    with open("genre_recommendations.json") as json_file:
        data = json.load(json_file)
        return data[genre]


def revise_input_data(data):
    S = pd.read_csv("Top_Smat.csv", index_col=0)
    R = pd.read_csv("Rmat.csv", index_col=0)
    M = pd.read_csv(
        "movies.dat", sep="::", engine="python", encoding="ISO-8859-1", header=None
    )
    M.columns = ["MovieID", "Title", "Genres"]

    movieIDs = list(map(lambda x: int(x[1:]), S.index))
    expanded_data = M.loc[M.MovieID.isin(movieIDs)]
    expanded_data = expanded_data.drop(columns=["Genres"])
    expanded_data["Rate"] = np.nan

    data = pd.DataFrame(data)
    for i in range(len(expanded_data)):
        ID = expanded_data.iloc[i]["MovieID"]
        if ID in data.MovieID.values:
            expanded_data.loc[expanded_data["MovieID"] == ID, "Rate"] = data[
                data["MovieID"] == ID
            ]["Rate"].values[0]

    expanded_data.index = expanded_data["MovieID"].values
    expanded_data = expanded_data.drop(columns=["MovieID", "Title"])
    expanded_data.index = map(lambda x: "m" + str(x), expanded_data.index)
    return expanded_data["Rate"]


def myIBCF(w):
    S = pd.read_csv("Top_Smat.csv", index_col=0)
    R = pd.read_csv("Rmat.csv", index_col=0)
    M = pd.read_csv(
        "movies.dat", sep="::", engine="python", encoding="ISO-8859-1", header=None
    )
    M.columns = ["MovieID", "Title", "Genres"]

    w_with_rate = w.dropna()
    rated_movies = w_with_rate.index
    predicted_ratings = w.copy()
    all_movies = S.index

    for movie in all_movies:
        if movie not in rated_movies:
            S_movie = S.loc[movie]  # Similarity of the movie
            S_movie_index = (
                S_movie.dropna().index
            )  # Only select movies with similarities
            useful_movies = S_movie_index.intersection(
                rated_movies
            )  # Further choose movies with both similarities and ratings
            # print(useful_movies)
            # print(w['m2196'])

            U = np.sum(S_movie[useful_movies] * predicted_ratings[useful_movies])
            D = np.sum(S_movie[useful_movies])

            if D != 0:
                predicted_ratings[movie] = U / D

    predicted_ratings = predicted_ratings.drop(rated_movies)
    res = predicted_ratings.sort_values(ascending=False)[:10]
    res.index = map(lambda x: int(x[1:]), res.index)
    res = res.sort_index()

    final_df = M[M["MovieID"].isin(res.index)]
    final_df = final_df.drop(columns=["Genres"])
    final_df["Rate"] = res.values
    final_df = final_df.sort_values(by=["Rate"], ascending=False)
    final_df = final_df.reset_index(drop=True)
    return final_df


def generate_output(res):
    output = []
    for i in range(len(res)):
        output.append(
            {"MovieID": res.iloc[i]["MovieID"], "Title": res.iloc[i]["Title"]}
        )
    return output


def System_2(input_data):
    revised_input = revise_input_data(
        input_data
    )  # convert input data from list of dictionary to series
    recommendations = myIBCF(revised_input)  # get recommendations
    final_output = generate_output(
        recommendations
    )  # format the recommendations to be a list of dictionary
    return final_output


def get_collaborative_recommendations(user_ratings):
    print(user_ratings)
    data = user_ratings
    # read necessary data
    S = pd.read_csv("Top_Smat_2.csv", index_col=0)
    M = pd.read_csv(
        "movies.dat", sep="::", engine="python", encoding="ISO-8859-1", header=None
    )
    M.columns = ["MovieID", "Title", "Genres"]
    data = pd.DataFrame(data)

    movieIDs = list(map(lambda x: int(x[1:]), S.index))
    data = pd.DataFrame(data)
    expanded_data = M.loc[M.MovieID.isin(movieIDs)]
    expanded_data = expanded_data.drop(columns=["Genres"])
    expanded_data["Rate"] = np.nan
    for i in range(len(expanded_data)):
        ID = expanded_data.iloc[i]["MovieID"]
        if ID in data.MovieID.values:
            expanded_data.at[i, "Rate"] = data[data["MovieID"] == ID]["Rate"].values[0]

    w = pd.Series(data=expanded_data["Rate"], index=expanded_data.MovieID.values)
    w.index = map(lambda x: "m" + str(x), w.index)

    all_movies = S.index
    rated_movies = w[~np.isnan(w)].index
    predicted_ratings = w.copy()

    for movie in all_movies:
        if movie not in rated_movies:
            predicted_ratings[movie] = np.nan

            S_movie = S.loc[movie]  # Similarity of the movie
            S_movie_index = S_movie[
                ~np.isnan(S_movie.values)
            ].index  # Only select movies with similarities
            useful_movies = S_movie_index.intersection(
                rated_movies
            )  # Further choose movies with both similarities and ratings

            U = np.sum(S_movie[useful_movies] * w[useful_movies])
            D = np.sum(S_movie[useful_movies])

            if D != 0:
                predicted_ratings[movie] = U / D

    predicted_ratings = predicted_ratings.drop(rated_movies)
    final_recommendation = predicted_ratings.sort_values(ascending=False)[:10]
    final_recommendation.index = map(lambda x: int(x[1:]), final_recommendation.index)

    selected_title = []
    for idx in final_recommendation.index:
        title = M[M.MovieID == idx]["Title"].values[0]
        selected_title.append(title)

    final_output = [
        {"MovieID": str(final_recommendation.index[i]), "Title": selected_title[i]}
        for i in range(len(final_recommendation))
    ]
    return final_output


if __name__ == "__main__":
    print(get_genre_recommendations("Action"))
