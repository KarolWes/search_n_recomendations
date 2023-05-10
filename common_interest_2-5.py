import pandas as pd

def common_interest(user: int, common_col_size: int):
    data = pd.read_csv("data_old/ratings_small.csv")
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
    common_interest(1, 5)