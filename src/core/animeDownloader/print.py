# ---- MODULES ----
from typing import List

from .animeFlv import AnimeInfo
# ----

# ---- FUNCTIONS ----

def PrintAnimes(animes:List[AnimeInfo], synopsis:bool=False, id:bool=False):
    """
    Print the anime information.
    """
    print("-- INFO --")

    for anime in animes:
        print(">>>")
        if id:
            print(f" · ID: {anime.id}")

        print(f" · Title: {anime.title}")
        print(f" · Ratings: {anime.rating}")

        if synopsis:
            print(f" · Synopsis: {anime.synopsis}")
        print(">>>")
    print("----")
# ----