# ---- MODULES ----
from src.core.animeDownloader.animeFlv import AnimeFlv


flv = AnimeFlv("Dragon Ball")

anime = flv.GetAnimeAt(2)

print(anime)