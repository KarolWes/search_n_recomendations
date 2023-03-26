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
                s+=float(line[2])
            mean = s/len(ratings)
            ratings.sort()
            if len(ratings)%2 == 0:
                median = (ratings[len(ratings)//2-1] + ratings[len(ratings)//2])/2
            else:
                median = ratings[len(ratings)//2]
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

def common_interest(user: int, common_col_size: int, filename:str, printout=True):
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
