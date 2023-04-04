import pandas as pd
import numpy as np
from utilityModule import *

def review_list(user_id:int):
    ratings = pd.read_csv("data/ratings_small.csv")
    ratings = ratings[ratings['userId'] == user_id]
    if len(ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    movies = movies_cleanup("data/movies.csv")
    review_movie = ratings.merge(movies, how="left")
    return review_movie


def cross_reference(user_id:int, common_size:int):
    ratings = pd.read_csv("data/ratings_small.csv")
    common_users = common_interest(user_id, common_size, "data/ratings_small.csv", printout=False)
    common_users.append(user_id)
    ratings = ratings[ratings['userId'].isin(common_users)]
    cross = ratings.pivot_table(values="rating",index="userId", columns="movieId")
    return cross


def norm(vec, p: int = 2):
    func = lambda x: pow(abs(x), p)
    res = sum(func(vec))
    return pow(res, (1/p))

def dot(X, Y):
    if len(X) != len(Y):
        raise NameError("Vectors of different length")
    tmp =[]
    for i in range(len(X)):
        tmp.append(X[i]*Y[i])
    return sum(tmp)


def cos_simil(X, Y):
    ans = 0
    try:
        d = dot(X, Y)
        nX = norm(X)
        nY = norm(Y)
        ans =  d/(nX*nY)
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
    newX = X[~nans]
    newY = Y[~nans]
    nans = np.isnan(newY)
    newX = X[~nans]
    newY = Y[~nans]
    return newX, newY
def generate_similarity_score(user_id, common_size):
    index_list = review_list(user_id)[['movieId']].T.values.tolist()[0]
    cross_tab = cross_reference(user_id, common_size)[index_list]
    users = cross_tab.index.tolist()
    users.remove(user_id)
    similarity_score = pd.DataFrame(0.0, index=users, columns=['score'])
    user_of_interest = cross_tab.loc[user_id].T.values.tolist()
    for u in users:
        vec = cross_tab.loc[u].T.values.tolist()
        X, Y = clean_vectors(user_of_interest, vec)
        similarity_score['score'][u] = cos_simil(X, Y)
    return similarity_score.sort_values(by='score', ascending=False)



if __name__ == "__main__":

    # print("Give the id of a user you want to predict for: ", end="")
    # user_id = int(input())
    # print(f"Some of the movies user {user_id} has rated:")
    # reviews = review_list(user_id)
    # print(reviews.head(10))

    print(generate_similarity_score(5, 12))
