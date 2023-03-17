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