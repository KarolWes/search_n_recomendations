from utilityModule import *


def private_interest_genres(reviews: pd.DataFrame):
    genres = generate_genres_dictionary_from_df(reviews, "rating", 3.0)
    if len(genres.keys()) == 0:
        return -1
    df = pd.DataFrame.from_dict(genres, orient="index", columns=["Count"])
    return df


def predict_simple(predict_size: int, reviews, genres_values: pd.DataFrame, mov_filename: str):
    reviewed = reviews["movieId_y"].T.values.tolist()
    all_movies = pd.read_csv(mov_filename)[["id", "original_title", "genres"]]
    to_predict = all_movies[~all_movies.id.isin(reviewed)].copy()
    to_predict["genres"] = to_predict["genres"].apply(cleanup_genres)
    overlap = []
    user_genre_list = genres_values.index
    for _, line in to_predict.iterrows():
        overlap.append(overlap_size(user_genre_list, line["genres"]))
    to_predict["overlap"] = overlap
    to_predict = to_predict.sort_values(by=["overlap"], ascending=False)
    return to_predict.head(predict_size)


def get_reviews(user_id: int, rev_filename: str, mov_filename: str):
    try:
        return review_list(user_id, rev_filename, mov_filename)
    except FileNotFoundError:
        return -1


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    print("Give the id of a user you want to predict for: ", end="")
    user_id = int(input())
    rev = get_reviews(user_id, "data/ratings.csv", "data/movies.csv")
    print(rev)
    genres_value_table = private_interest_genres(rev)
    print(predict_simple(10, rev, genres_value_table, "data/movies.csv"))
