import csv


def analyze_movies(name):
    try:
        f = open(name, mode="r", encoding="utf-8")
    except FileNotFoundError:
        print("File not found")
        return -1
    genres = {}
    lines = csv.DictReader(f, delimiter=',', quotechar='"')
    for row in lines:
        try:
            genre_list = row['genres'].strip().split('|')
            for g in genre_list:
                genres[g] = genres.get(g, 0)+1
        except IndexError:
            print("File has a wrong structure")
            f.close()
            return -1
    print(f"All genres: {[*genres.keys()]}")
    genres = sorted(genres.items(), key=lambda x:x[1], reverse=True)
    print("Occurances: ")
    for key, count in genres:
        print(f"{key}: {count} times")
    f.close()
    return 1


if __name__ == '__main__':
    print(analyze_movies("data/movies.csv"))
