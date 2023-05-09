# well known constants

# data
MOVIE_FILE = "C:/Users/Karol/Documents/Python Scripts/search&recomandation/assignment6/polls/data/movies.csv"
RATINGS_SMALL_FILE = "C:/Users/Karol/Documents/Python Scripts/search&recomandation/assignment6/polls/data/ratings_small.csv"
RATINGS_FILE = ""
RECOMENDATION_SITE_TEMPLATE ="C:/Users/Karol/Documents/Python Scripts/search&recomandation/assignment6/polls/templates/assignment6/secondpage.html"
CREDIT_FILE = "C:/Users/Karol/Documents/Python Scripts/search&recomandation/assignment6/polls/data/credits.csv"
API_KEY = "a24c6dc45c80e92d954b8f95378bb27a"

# macros
def MOVIE_REQUEST(n):
    return f"https://api.themoviedb.org/3/movie/{n}/images?api_key=a24c6dc45c80e92d954b8f95378bb27a"


def POSTER(n):
    return f"https://image.tmdb.org/t/p/original/{n}"
