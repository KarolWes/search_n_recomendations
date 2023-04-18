import pandas as pd
import numpy as np
from utilityModule import *


def review_list(user_id: int):
    ratings = pd.read_csv("data/ratings_small.csv")
    user_ratings = ratings[ratings['userId'] == user_id]
    if len(user_ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    movies = movies_cleanup("data/movies.csv")
    review_movie = user_ratings.merge(movies, how="left")
    return review_movie


def cross_reference(user_id: int, common_size: int):
    ratings = pd.read_csv("data/ratings_small.csv")
    common_users = common_interest(user_id, common_size, "data/ratings_small.csv", printout=False)
    common_users.append(user_id)
    ratings = ratings[ratings['userId'].isin(common_users)]
    cross = ratings.pivot_table(values="rating", index="userId", columns="movieId")
    return cross


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
    except ZeroDivisionError:
        print("Vectors are perpendicular")
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


def predict_ratings(user_id: int, num_similar_users: int, num_movies: int):
    # get the movie ratings for the user of interest
    index_list = review_list(user_id)[['movieId']].T.values.tolist()[0]
    cross_tab = cross_reference(user_id, num_similar_users)[index_list]

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
    ratings = pd.read_csv("data/ratings_small.csv")
    similar_user_ratings = ratings[ratings['userId'].isin(most_similar_users)]
    similar_user_ratings = similar_user_ratings[~similar_user_ratings['movieId'].isin(index_list)]

    to_predict = [*set(similar_user_ratings['movieId'].values.tolist())]

    # compute the predicted rating for each movie
    predicted_ratings = []
    for movie_id in to_predict:
        movie_ratings = similar_user_ratings[similar_user_ratings['movieId'] == movie_id]['rating']
        if len(movie_ratings) > 0:
            predicted_rating = movie_ratings.mean()
        else:
            predicted_rating = 0
        predicted_ratings.append((movie_id, predicted_rating))

    # sort the list of predicted ratings by descending score
    predicted_ratings.sort(key=lambda x: x[1], reverse=True)

    # get the top N movies with the highest predicted rating
    top_movies = predicted_ratings[:num_movies]

    # merge the movie titles and genres onto the list of top movies
    movies = movies_cleanup("data/movies.csv")
    top_movies = pd.DataFrame(top_movies, columns=['movieId', 'predicted_rating'])
    top_movies = top_movies.merge(movies, how='left')

    return top_movies


if __name__ == "__main__":
    print("Give the id of a user you want to predict for: ", end="")
    user_id = int(input())
    print(f"Some of the movies user {user_id} has rated:")
    reviews = review_list(user_id)
    print(reviews.head(10))
    print("Highest predicted relevance score")
    ans = predict_ratings(5, 15, 25)
    print(ans)
    ans.to_csv("data/output.csv", index=False)