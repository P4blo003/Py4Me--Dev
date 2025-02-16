# ---- MODULES ----
from src.core.animeDownloader import AnimeFlv
# ----

# ---- MAIN ----
if __name__ == "__main__":

    animeDownloader = AnimeFlv()

    animes = animeDownloader.Search("Dragon")
# ----