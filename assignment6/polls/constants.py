# well known constants

# data_old
MOVIE_FILE = "polls/data/movies.csv"
RATINGS_SMALL_FILE = "polls/data/ratings_small.csv"
RATINGS_FILE = ""
CREDIT_FILE = "polls/data/credits.csv"
RECOMENDATION_SITE_TEMPLATE = "assignment6/secondpage.html"
API_KEY = "a24c6dc45c80e92d954b8f95378bb27a"

# macros
def MOVIE_REQUEST(n):
    return f"https://api.themoviedb.org/3/movie/{n}/images?api_key=a24c6dc45c80e92d954b8f95378bb27a"


def POSTER(n):
    return f"https://image.tmdb.org/t/p/original/{n}"
