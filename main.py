# ---- MODULES ----
from src.core.animeDownloader import AnimeFlv
from src.core.animeDownloader import PrintAnimes
# ----

# ---- MAIN ----
if __name__ == "__main__":

    animeDownloader = AnimeFlv()

    animes = animeDownloader.Search("Dragon Ball")

    PrintAnimes(animes=animes)
# ----