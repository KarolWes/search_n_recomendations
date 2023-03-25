import numpy
import pandas as pd


def to_float(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return numpy.nan


def task2_1():
    data = ['Toy Story', 'Jumanji', 'Grumpier Old Men']
    data = pd.Series(data)
    print(data[0])
    print()
    print(data[[0, 1]])
    print()
    print(data.iloc[[-1, -2]])
    print()
    data.index = ['a', 'b', 'c']
    print(data[['b']])


def task2_2():
    data = [['Jumanji', 17.015539], ['Toy Story', 21.946943], ['Grumpier Old Men', 11.7129]]
    data = pd.DataFrame(data)
    data.columns = ['title', 'popularity']
    print(data.head())
    print()
    data = data.sort_values(["popularity"], axis=0)
    print(data.head())
    print()
    print(data["popularity"])
    print()


def task2_3():
    data = pd.read_csv("data/movies_metadata.csv")
    print(type(data))
    print(data.iloc[0])
    print()
    print(data.iloc[-1])
    print()
    print(data.loc[data["title"] == "Jumanji"])
    print()
    # -------------
    data_small = data[['title', 'release_date', 'popularity', 'revenue', 'runtime', 'genres']].copy()
    print(data_small.head())
    data_small.loc['release_date'] = pd.to_datetime(data_small['release_date'], errors='coerce')
    data_small['release_year'] = data_small['release_date'].apply(
        lambda x: to_float(str(x).split('-')[0] if x != numpy.nan else numpy.nan))
    data_small['release_year'] = data_small['release_year'].astype('float')
    data_small = data_small.drop(columns="release_date")
    print(data_small.loc[data_small['release_year'] > 2010].head())


def task2_4():
    data = pd.read_csv("data/ratings_small.csv")
    data = data.groupby("movieId").rating.agg(["mean", "median"])
    data.columns = ["rating_mean", "rating_median"]
    print(data.head())
    ans = []
    for index, row in data.iterrows():
        d = {"id": index, "rating_mean": row["rating_mean"], "rating_median": row["rating_median"]}
        ans.append(d)
    return ans


def task2_5(user: int, common_col_size: int):
    data = pd.read_csv("data/ratings_small.csv")
    data = data.groupby("userId")
    all_users = list(data.groups.keys())
    try:
        all_users.remove(user)
        user_of_interest = set(data.get_group(user)["movieId"])
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
        print(f"Users with at least {common_col_size} common movies as user of interest: {other_users}")
    except ValueError:
        print("User with given Id doesn't exist")


if __name__ == "__main__":
    # task2_1()
    # print("___")
    # task2_2()
    # print("___")
    # task2_3()
    # print("___")
    # print(task2_4())
    # print("___")
    print(task2_5(1, 5))

