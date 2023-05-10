from assignment6.polls import constants as cs
from utilityModule import *


C = 10


def cross_reference(user_id: int, ratings:pd.DataFrame, common_size: int=10):
    common_users = common_interest(user_id, common_size, ratings, printout=False)
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


def predict_ratings(user_id: int, review_list:pd.DataFrame, num_similar_users: int=10, num_movies: int=20):
    ratings = pd.read_csv(cs.RATINGS_SMALL_FILE)
    # get the movie ratings for the user of interest
    index_list = review_list[['movieId_x']].T.values.tolist()[0]
    cross_tab = cross_reference(user_id, ratings,  num_similar_users)[index_list]

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
    print(similarity_scores)
    most_similar_users = [x[0] for x in similarity_scores][:num_similar_users]

    # get the ratings for the most similar users

    similar_user_ratings = ratings[ratings['userId'].isin(most_similar_users)]
    similar_user_ratings = similar_user_ratings[~similar_user_ratings['movieId'].isin(index_list)]

    to_predict = [*set(similar_user_ratings['movieId'].values.tolist())]

    # compute the predicted rating for each movie
    predicted_ratings = []
    for movie_id in to_predict:
        movie_ratings = similar_user_ratings[similar_user_ratings['movieId'] == movie_id]['rating']
        if len(movie_ratings) > min(3, len(users)//2):
            predicted_rating = movie_ratings.mean()
        else:
            predicted_rating = np.NaN
        predicted_ratings.append((movie_id, predicted_rating))

    # sort the list of predicted ratings by descending score
    predicted_ratings.sort(key=lambda x: x[1], reverse=True)

    # merge the movie titles and genres onto the list of top movies
    movies = movies_cleanup(cs.MOVIE_FILE)
    top_movies = pd.DataFrame(predicted_ratings, columns=['movieId', 'predicted_rating']).merge(movies, how='left').dropna()\
        .sort_values("predicted_rating", ascending=False)[:num_movies]


    return top_movies


if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    print("Give the id of a user you want to predict for: ", end="")
    user_id = int(input())
    print(f"Some of the movies user {user_id} has rated:")
    reviews = review_list(user_id, cs.RATINGS_SMALL_FILE, cs.MOVIE_FILE)
    print(reviews.head(10))
    print("Highest predicted relevance score")
    ans = predict_ratings(user_id, reviews, num_similar_users=15, num_movies=20)
    cast = pd.read_csv(cs.CREDIT_FILE, usecols=['cast', 'id'])[['id','cast']]
    ans = ans.merge(cast, how="left", left_on="movieId", right_on="id")
    cast = extract_cast(ans)
    ans = ans.drop("cast", axis=1)
    ans = ans.merge(cast, left_on="movieId", right_index=True)
    print(ans)
