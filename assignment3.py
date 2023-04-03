import pandas as pd
import numpy as np
from utilityModule import common_interest

def review_list(user_id:int):
    ratings = pd.read_csv("data/ratings.csv")
    ratings = ratings[ratings['userId'] == user_id]
    if len(ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    movies = pd.read_csv("data/movies.csv")
    review_movie = ratings.merge(movies)
    return review_movie


def cross_reference(user_id:int, common_size:int):
    ratings = pd.read_csv("data/ratings.csv")
    common_users = common_interest(user_id, common_size, "data/ratings.csv", printout=False)
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



if __name__ == "__main__":
    # print("Give the id of a user you want to predict for: ", end="")
    # user_id = int(input())
    # print(f"Some of the movies user {user_id} has rated:")
    # print(review_list(user_id)[["title", "genres"]].head(n=15))

    # print(cross_reference(1, 10))
    X = np.array([1,1,1,1])
    Y = np.array([5,5,5,5])
    print(cos_simil(X, Y))
