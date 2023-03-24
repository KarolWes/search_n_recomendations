import pandas as pd

def review_list(user_id:int):
    ratings = pd.read_csv("data/ratings.csv")
    ratings = ratings[ratings['userId'] == user_id]
    if len(ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    movies = pd.read_csv("data/movies.csv")
    review_movie = ratings.merge(movies)
    return review_movie


if __name__ == "__main__":
    print("Give the id of a user you want to predict for: ", end="")
    user_id = int(input())
    print(f"Some of the movies user {user_id} has rated:")
    print(review_list(user_id)[["title", "genres"]].head(n=15))
