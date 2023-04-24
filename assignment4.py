import pandas as pd

from utilityModule import *


def private_interest_genres(reviews: pd.DataFrame):
    genres = generate_genres_dictionary_from_df(reviews, "rating", 3.0)
    if len(genres.keys()) == 0:
        return -1
    df = pd.DataFrame.from_dict(genres, orient="index", columns=["Count"])
    return df


def predict_simple(predict_size: int, reviews, genres_values: pd.DataFrame, mov_filename: str):
    to_predict = get_to_predict_movies(mov_filename, reviews)
    overlap = []
    user_genre_list = genres_values.index
    for _, line in to_predict.iterrows():
        overlap_length = overlap_size(user_genre_list, line["genres"]);
        if overlap_length > 0:
            overlap.append(overlap_length)
    to_predict["overlap"] = pd.Series(overlap)

    # count the number of ratings for each remaining items
    ratings = pd.read_csv("data/ratings_small.csv")
    remaining_ratings = ratings.merge(to_predict, left_on="movieId", right_on="id")
    item_counts = remaining_ratings.groupby("id").count()[["rating"]]
    item_counts.columns = ["count"]

    # Rank the remaining items by popularity
    to_predict = to_predict.merge(item_counts, left_on="id", right_index=True)
    to_predict = to_predict.sort_values(by=["count", "overlap"], ascending=False)

    return to_predict.head(predict_size)


def predict_with_genre_count(predict_size: int, reviews, genres_values: pd.DataFrame, mov_filename: str):
    to_predict = get_to_predict_movies(mov_filename, reviews)
    genre_counts = []

    for _, line in to_predict.iterrows():
        count = 0
        for genre in line["genres"]:
            if genre in genres_values.index:
                count += genres_values.loc[genre][0]
        genre_counts.append(count)

    to_predict["genre_count"] = pd.Series(genre_counts)
    to_predict = to_predict.sort_values(by=["genre_count"], ascending=False)

    return to_predict.head(predict_size)


def get_to_predict_movies(mov_filename, reviews):
    reviewed = reviews["movieId_y"].T.values.tolist()
    all_movies = pd.read_csv(mov_filename)[["id", "original_title", "genres"]]
    to_predict = all_movies[~all_movies.id.isin(reviewed)]
    to_predict["genres"] = to_predict["genres"].apply(cleanup_genres)
    return to_predict


def get_reviews(user_id: int, rev_filename: str, mov_filename: str):
    try:
        return review_list(user_id, rev_filename, mov_filename)
    except FileNotFoundError:
        return -1


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    print("Give the id of a user you want to predict for: ", end="")
    user_id = int(input())
    rev = get_reviews(user_id, "data/ratings_small.csv", "data/movies.csv")
    print(rev)
    genres_value_table = private_interest_genres(rev)
    print(predict_simple(10, rev, genres_value_table, "data/movies.csv"))
    print(predict_with_genre_count(10, rev, genres_value_table, "data/movies.csv"))
