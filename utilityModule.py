import random

import numpy
import numpy as np
import pandas as pd


def calculate_mode(data):
    values = {}
    for entry in data:
        values[entry] = values.get(entry, 0) + 1
    return sorted(values.items(), key=lambda x: x[1], reverse=True)[0][0]


class Statistics:
    def __init__(self, name):
        self.name = name

    def mean_rating(self):
        try:
            f = open(self.name, "r")
        except FileNotFoundError:
            print("File not found")
            return -1
        ratings = []
        lines = f.readlines()
        try:
            lines = lines[1:]
        except IndexError:
            print("File was empty")
            f.close()
            return -1
        s = 0
        mean = -10
        median = None
        mode = None
        try:
            for line in lines:
                line = line.split(',')
                ratings.append(float(line[2]))
                s += float(line[2])
            mean = s / len(ratings)
            ratings.sort()
            if len(ratings) % 2 == 0:
                median = (ratings[len(ratings) // 2 - 1] + ratings[len(ratings) // 2]) / 2
            else:
                median = ratings[len(ratings) // 2]
            mode = calculate_mode(ratings)

        except ValueError:
            print("Couldn't convert string to float")
            mean = -1
        except IndexError:
            print("Index out of bound - file has a wrong structure")
            mean = -1
        except ZeroDivisionError:
            print("File was empty")
            mean = -1
        finally:
            f.close()
        return mean, median, mode


def common_interest(user: int, common_col_size: int, filename: str, printout=True):
    data = pd.read_csv(filename)
    data = data.groupby("userId")
    all_users = list(data.groups.keys())
    try:
        all_users.remove(user)
        user_of_interest = set(data.get_group(user)["movieId"])
        if printout:
            print(f"Collection of user of interest: {user_of_interest}")
        if len(user_of_interest) < common_col_size:
            print(f"Size of common collection ({common_col_size}) "
                  f"is bigger than size of collection of user of interest ({len(user_of_interest)})")
            return
        other_users = []
        for id in all_users:
            id_collection = set(data.get_group(id)["movieId"])
            common = user_of_interest.intersection(id_collection)
            if len(common) >= common_col_size:
                other_users.append(id)
        if printout:
            print(f"Users with at least {common_col_size} common movies as user of interest: {other_users}")
        return other_users
    except ValueError:
        print("User with given Id doesn't exist")
        return


def movies_cleanup(filename: str):
    try:
        data = pd.read_csv(filename, usecols=['id', 'title', 'genres'], dtype={'id': 'int64', 'title': 'string'})[
            ['id', 'title', 'genres']]
    except FileNotFoundError:
        raise FileNotFoundError
    data = data.rename(columns={"id": "movieId"})
    return data


def to_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return numpy.nan


def generate_genre_dictionary_from_file(filename: str):
    genres = {}
    df = pd.DataFrame(pd.read_csv(filename, converters={"genres": lambda x: x.strip("[]").split(", ")}))
    g = df['genres']
    for line in g:
        for el in line:
            el = el.strip("{}").split(': ')
            if el[0].strip("''") == "name":
                genres[el[1].strip("''")] = genres.get(el[1].strip("''"), 0) + 1
    return genres


def generate_genres_dictionary_from_df(data: pd.DataFrame, param_col: str, param_val, col_name="genres", ):
    genres = {}
    for _, line in data.iterrows():
        if line[param_col] > param_val:
            g = line["genres"]
            if type(g) == str:
                g = g.strip("[]").split(", ")
                for el in g:
                    el = el.strip("{}").split(": ")
                    if el[0].strip("''") == "name":
                        genres[el[1].strip("''")] = genres.get(el[1].strip("''"), 0) + 1
    return genres


def review_list(user_id: int, rev_filename: str, mov_filename: str):
    try:
        ratings = pd.read_csv(rev_filename)
    except FileNotFoundError:
        print("File reviews not found")
        return None
    user_ratings = ratings[ratings['userId'] == user_id]
    if len(user_ratings) == 0:
        print(f"User with given id ({user_id}) does not exist")
        return None
    try:
        movies = movies_cleanup(mov_filename)
    except FileNotFoundError:
        print("File movies not found")
        return None
    movies.index += 1
    review_movie = user_ratings.merge(movies, how="left", left_on="movieId", right_index=True)
    return review_movie


def cleanup_genres(line: str):
    res = []
    line = line.strip('[]').split(", ")
    for el in line:
        el = el.strip("{}").split(": ")
        if el[0].strip("''") == "name":
            res.append(el[1].strip("''"))
    return res


def split_dataset(filename, training_ratio):
    if training_ratio > 1:
        raise Exception("Training radio must be <= 1")
    try:
        dataset = pd.read_csv(filename)
        dataset_len = len(dataset)
        training_size = int(dataset_len * training_ratio)
        dataset_arr = np.array(dataset)
        random.shuffle(dataset_arr)
        return pd.DataFrame(dataset[:training_size]), pd.DataFrame(dataset[training_size:])
    except FileNotFoundError:
        print("File not found")
        return None



def overlap_size(A, B):
    return len(set(A).intersection(set(B)))
