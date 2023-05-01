import pandas as pd

import constants as cs
from utilityModule import *

def add_titles(reviews:pd.DataFrame, movie_filename):
    try:
        movies = movies_cleanup(movie_filename)
    except FileNotFoundError:
        print("File movies not found")
        return None
    movies.index += 1
    review_movie = reviews.merge(movies, how="left", left_on="movieId", right_index=True)
    review_movie = review_movie[["userId", "movieId_x", "title", "rating"]]
    review_movie.columns = ["userId", "movieId", "title", "rating"]
    return review_movie

def get_user_ratings(dataframe):
    user_ratings_dict = {}
    for index, row in dataframe.iterrows():
        user_id = row["userId"]
        movie_id = row["movieId"]
        rating = row["rating"]
        if user_id not in user_ratings_dict:
            user_ratings_dict[user_id] = {}
        user_ratings_dict[user_id][movie_id] = rating
    return user_ratings_dict


# Calculate the similarity between two users based on their movie ratings
def calculate_similarity(user1, user2, us_ratings):
    if user1 not in us_ratings or user2 not in us_ratings:
        return 0
    movies1 = set(us_ratings[user1].keys())
    movies2 = set(us_ratings[user2].keys())
    common_movies = movies1.intersection(movies2)
    if len(common_movies) == 0:
        return 0
    common_movies = set(us_ratings[user1]).intersection(set(us_ratings[user2]))
    if len(common_movies) == 0:
        return 0
    user1_ratings = [us_ratings[user1][movie] for movie in common_movies]
    user2_ratings = [us_ratings[user2][movie] for movie in common_movies]
    num = sum([a * b for a, b in zip(user1_ratings, user2_ratings)])
    denom1 = sum([rating ** 2 for rating in user1_ratings])
    denom2 = sum([rating ** 2 for rating in user2_ratings])
    denom = (denom1 ** 0.5) * (denom2 ** 0.5)
    if denom == 0:
        return 0
    return num / denom


# predict the rating of the user for a movie
def predict_rating(user_id, movie_id, us_ratings):
    numerator = 0
    denominator = 0
    for other_user in us_ratings:
        if other_user != user_id and movie_id in us_ratings[other_user]:
            similarity = calculate_similarity(user_id, other_user, us_ratings)
            numerator += similarity * us_ratings[other_user][movie_id]
            denominator += similarity
    if denominator == 0:
        return 0
    return numerator / denominator


# Make predictions for each user-item pair in the test set
def make_predictions(test_df, us_ratings):
    predictions = []
    for index, row in test_df.iterrows():
        user_id = row["userId"]
        movie_id = row["movieId"]
        prediction = predict_rating(user_id, movie_id, us_ratings)
        predictions.append((user_id, prediction))
    return predictions


def predictions_readable(predictions, test_df):
    i = 0
    for _, row in test_df.iterrows():
        movie_title = row["title"]
        p = predictions[i]
        if p[1] > 0:
            print(f"user {p[0]} -> {movie_title}: {p[1]}")
        i+=1


def compute_mea(test_df, predictions):
    actual_ratings = list(test_df["rating"])
    return sum([abs(actual - pred[1]) for actual, pred in zip(actual_ratings, predictions)]) / len(actual_ratings)


def compute_rmse(test_df, predictions):
    actual_ratings = list(test_df["rating"])
    return np.sqrt(sum([(actual - pred[1]) ** 2 for actual, pred in zip(actual_ratings, predictions)]) / len(actual_ratings))


def task1(ratio: float):
    train_data, test_data = split_dataset(cs.RATINGS_SMALL_FILE, ratio)
    train_data = add_titles(train_data, cs.MOVIE_FILE)
    test_data = add_titles(test_data, cs.MOVIE_FILE)
    user_ratings = get_user_ratings(train_data)
    ratings_predictions = make_predictions(test_data, user_ratings)
    predictions_readable(ratings_predictions, test_data)
    mea = compute_mea(test_data, ratings_predictions)
    rmse = compute_rmse(test_data, ratings_predictions)
    print(mea)
    print(rmse)

def precission():
    # true positive / all
    pass

def recall():
    # true positive / false negative
    pass

def task2():
    train_data, test_data = split_dataset(cs.RATINGS_SMALL_FILE, 0.2)
    user_ratings = get_user_ratings(train_data)
    ratings_predictions = make_predictions(test_data, user_ratings)


if __name__ == "__main__":
    print("Enter training-set ratio between 0 and 1: ")
    ratio = float(input())
    task1(ratio)



