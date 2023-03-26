import pandas as pd
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



if __name__ == "__main__":
    # print("Give the id of a user you want to predict for: ", end="")
    # user_id = int(input())
    # print(f"Some of the movies user {user_id} has rated:")
    # print(review_list(user_id)[["title", "genres"]].head(n=15))

    print(cross_reference(1, 10))
