# ---- MODULES ----
from src.core.animeDownloader.animeFlv import AnimeFlv




ad = AnimeFlv()
animes = ad.LookFor("Dragon BAll")

for index, anime in enumerate(animes):

    print(f"<<{index}>>")
    print(f" · Title: {anime.title}")
    print(f" · Query: {anime.queryUrl}")
    print(f" · Type: {anime.animeType}")
    print()