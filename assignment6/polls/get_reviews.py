import numpy as np
import pandas as pd
from . import constants as cs
import requests


"""
This file is created with the code used in previous exercises, adjusted to the needs of django
"""

def movies_cleanup(filename: str):
    try:
        data = pd.read_csv(filename, usecols=['id', 'title', 'genres', 'overview'],
                           dtype={'id': 'int64', 'title': 'string'})[
            ['id', 'title', 'genres', 'overview']]
    except FileNotFoundError:
        raise FileNotFoundError
    data = data.rename(columns={"id": "movieId", "overview": "synopsis"})
    return data


def extract_cast(data: pd.DataFrame, col_name="cast", lim=4):
    output = {}
    for _, line in data.iterrows():
        cast = line[col_name]
        id = line["movieId"]
        if type(cast) == str:
            output[id] = []
            cast = cast.strip("[]").split(", ")
            for member in cast:
                member = member.strip("{}").split(", ")
                for field in member:
                    field = field.split(": ")
                    if field[0].strip("''") == "name":
                        output[id].append(field[1].strip("''"))
                if len(output[id]) >= 4:
                    break
    res = pd.DataFrame([output]).T
    res.columns = ["cast"]
    return res

def extract_genres(data: pd.DataFrame, col_name="genres", ):
    output = {}
    for _, line in data.iterrows():
        id = line["movieId"]
        g = line[col_name]
        if type(g) == str:
            output[id] = []
            g = g.strip("[]").split(", ")
            for el in g:
                el = el.strip("{}").split(": ")
                if el[0].strip("''") == "name":
                    output[id].append(el[1].strip("''"))
    res = pd.DataFrame([output]).T
    res.columns = ["genres"]
    return res


def norm(vec, p: int = 2):
    func = lambda x: pow(abs(x), p)
    res = sum(func(vec))
    return pow(res, (1 / p))


def dot(X, Y):
    if len(X) != len(Y):
        raise NameError("Vectors of different length")
    tmp = []
    for i in range(len(X)):
        tmp.append(X[i] * Y[i])
    return sum(tmp)


def cos_simil(X, Y):
    ans = 0
    try:
        d = dot(X, Y)
        nX = norm(X)
        nY = norm(Y)
        ans = d / (nX * nY)
    except NameError as nerr:
        print(nerr)
        return None
    except ZeroDivisionError:
        print("Vectors are perpendicular")
        return None
    finally:
        return ans


def clean_vectors(X, Y):
    if len(X) != len(Y):
        raise NameError("Vectors of different length")
    X = np.array(X)
    Y = np.array(Y)
    nans = np.isnan(X)
    newY = Y[~nans]
    nans = np.isnan(newY)
    newX = X[~nans]
    newY = Y[~nans]
    return newX, newY


def common_interest(user: int, common_col_size: int, data: pd.DataFrame):
    data = data.groupby("userId")
    all_users = list(data.groups.keys())
    try:
        all_users.remove(user)
        user_of_interest = set(data.get_group(user)["movieId"])
        if len(user_of_interest) < common_col_size:
            print(f"Size of common collection ({common_col_size}) "
                  f"is bigger than size of collection of user of interest ({len(user_of_interest)})")
            return None
        other_users = []
        for id in all_users:
            id_collection = set(data.get_group(id)["movieId"])
            common = user_of_interest.intersection(id_collection)
            if len(common) >= common_col_size:
                other_users.append(id)
        return other_users
    except ValueError:
        print("User with given Id doesn't exist")
        return None


def cross_reference(user_id: int, ratings: pd.DataFrame, common_size: int = 10):
    common_users = common_interest(user_id, common_size, ratings)
    common_users.append(user_id)
    ratings = ratings[ratings['userId'].isin(common_users)]
    cross = ratings.pivot_table(values="rating", index="userId", columns="movieId")
    return cross


def review_list(user_id: int, rev_filename: str, mov_filename: str):
    try:
        ratings = pd.read_csv(rev_filename)
    except FileNotFoundError:
        print("File reviews not found")
        return None
    user_ratings = ratings[ratings['userId'] == user_id]
    if len(user_ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    try:
        movies = movies_cleanup(mov_filename)
    except FileNotFoundError:
        print("File movies not found")
        return None
    movies.index += 1
    review_movie = user_ratings.merge(movies, how="left", left_on="movieId", right_index=True) \
        .sort_values("rating", ascending=False).dropna()

    return review_movie


def predict_ratings(user_id: int, review_list: pd.DataFrame, num_similar_users: int = 10, num_movies: int = 20):
    ratings = pd.read_csv(cs.RATINGS_SMALL_FILE)
    # get the movie ratings for the user of interest
    index_list = review_list[['movieId_x']].T.values.tolist()[0]
    cross_tab = cross_reference(user_id, ratings, 5)[index_list]

    # get the list of the users with similar ratings
    users = cross_tab.index.tolist()
    users.remove(user_id)

    # compute the similarity score between the user of interest and each similar user
    similarity_scores = []
    user_of_interest = cross_tab.loc[user_id].T.values.tolist()
    for u in users:
        vec = cross_tab.loc[u].T.values.tolist()
        X, Y = clean_vectors(user_of_interest, vec)
        similarity_scores.append((u, cos_simil(X, Y)))

    # sort the list of similar users by descending similarity score
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [x[0] for x in similarity_scores][:num_similar_users]

    # get the ratings for the most similar users

    similar_user_ratings = ratings[ratings['userId'].isin(most_similar_users)]
    similar_user_ratings = similar_user_ratings[~similar_user_ratings['movieId'].isin(index_list)]

    to_predict = [*set(similar_user_ratings['movieId'].values.tolist())]

    # compute the predicted rating for each movie
    predicted_ratings = []
    for movie_id in to_predict:
        movie_ratings = similar_user_ratings[similar_user_ratings['movieId'] == movie_id]['rating']
        if len(movie_ratings) > min(3, len(users) // 2):
            predicted_rating = movie_ratings.mean()
        else:
            predicted_rating = np.NaN
        predicted_ratings.append((movie_id, predicted_rating))

    # sort the list of predicted ratings by descending score
    predicted_ratings.sort(key=lambda x: x[1], reverse=True)

    # merge the movie titles and genres onto the list of top movies
    movies = movies_cleanup(cs.MOVIE_FILE)
    top_movies = pd.DataFrame(predicted_ratings, columns=['movieId', 'predicted_rating']) \
                     .merge(movies, how='left').dropna() \
                     .sort_values("predicted_rating", ascending=False)[:num_movies]
    return top_movies


def extract_pic_url(data, id_col):
    ids = data[id_col]
    output = {}
    for id in ids:
        url = cs.MOVIE_REQUEST(id)
        headers = {
            "Authorization": f"Bearer {cs.API_KEY}"}
        response = requests.get(url, headers=headers).json()
        output[id] = cs.POSTER(response["posters"][0]['file_path'])
    res = pd.DataFrame([output]).T
    res.columns = ["poster"]
    return res



def prepare_for_output(user: int, review_list: pd.DataFrame, num_similar_users: int = 10, num_movies: int = 20):
    ratings = predict_ratings(user, review_list, num_similar_users, num_movies)
    cast = pd.read_csv(cs.CREDIT_FILE, usecols=['id', 'cast'])[["id", "cast"]]
    ans = ratings.merge(cast, how="left", left_on="movieId", right_on="id")
    cast = extract_cast(ans)
    gen = extract_genres(ans)
    poster = extract_pic_url(ans, "movieId")
    ans = ans.drop("cast", axis=1)
    ans = ans.drop("genres", axis=1)
    ans = ans.merge(cast, left_on="movieId", right_index=True)
    ans = ans.merge(gen, left_on="movieId", right_index=True)
    ans = ans.merge(poster, left_on="movieId", right_index=True)

    return ans
