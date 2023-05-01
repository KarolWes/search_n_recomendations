import constants as cs
from utilityModule import *


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
    movies1 = set(user_ratings[user1].keys())
    movies2 = set(user_ratings[user2].keys())
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
        predictions.append(prediction)
    return predictions


def compute_mea(test_df, predictions):
    actual_ratings = list(test_df["rating"])
    return sum([abs(actual - pred) for actual, pred in zip(actual_ratings, predictions)]) / len(actual_ratings)


def compute_rmse(test_df, predictions):
    actual_ratings = list(test_df["rating"])
    return np.sqrt(sum([(actual - pred) ** 2 for actual, pred in zip(actual_ratings, predictions)]) / len(actual_ratings))


if __name__ == "__main__":
    print("Enter training-set ratio between 0 and 1: ")
    ratio = float(input())
    train_data, test_data = split_dataset(cs.RATINGS_SMALL_FILE, ratio)
    user_ratings = get_user_ratings(train_data)
    ratings_predictions = make_predictions(test_data, user_ratings)
    print(ratings_predictions)
    mea = compute_mea(test_data, ratings_predictions)
    rmse = compute_rmse(test_data, ratings_predictions)
    print(mea)
    print(rmse)

