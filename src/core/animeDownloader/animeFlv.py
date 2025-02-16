# ---- MODULES ----
from src.utils.file import getDataFromJSON

import cloudscraper
from bs4 import BeautifulSoup, ResultSet
from dataclasses import dataclass
from typing import Optional, List
from urllib.parse import urlencode
# ----

# ---- DATA CLASSES ----
@dataclass
class EpisodeInfo:
    """
    Episode information.
    """
    id:str
    name:str
    anime:str

@dataclass
class DownloadLinkInfo:
    """
    Download link information.
    """
    server:str
    url:str

@dataclass
class AnimeInfo:
    """
    Anime information.
    """
    id:str
    title:str
    synopsis:Optional[str] = None
    rating:Optional[str] = None
    episodes:Optional[List[EpisodeInfo]] = None
# ----


# ---- CLASSES ----
class AnimeFlv:

    # ---- DEFAULT METHODS ----
    def __init__(self, session:str=None):
        """
        Initializes the class properties.
        """
        # Default properties
        self.__webUrl = None        # AnimeFlv web url.
        self.__browseUrl = None     # AnimeFlv search url.

        self.__scrapper = cloudscraper.create_scraper(sess=session)
        self.__loadSettings()     # Load the settings.

    def __repr__(self):
        """
        Returns the string representation of the objetc.
        """
        return f"AnimeFlv:\n · Web: {self.__webUrl}"

    def __exit__(self):
        """
        Method called when exit.
        """
        self.__scrapper.close() # Close the
    # ----

    # ---- PROPERTIES ----
    @property
    def webUrl(self) -> str:
        """
        Gets the web url
        """
        return self.__webUrl
    # ----

    # ---- PRIVATE METHODS ----
    def __loadSettings(self):
        """
        Load the settings from the JSON file.
        """
        data = getDataFromJSON("/home/pablo/Projects/Py4Me/src/core/animeDownloader/settings.json")
        self.__webUrl = data.get('web_url')
        self.__browseUrl = data.get('browse_url')

    def __processAnimesInfo(self, elements:ResultSet) -> List[AnimeInfo]:
        """
        Process the resultSet and returns the list with the animes.
        
        :param ResultSet elements:
            Result of elements get by query.
        """
        
        animes = []

        for element in elements:
            
            id = element.select_one("div.Description a.Button")["href"]
            title = element.select_one("a h3.Title").string
            synopsis = element.select("div.Description p")[1].string
            rating = element.select_one("div.Description p span.Vts").string

            animes.append(AnimeInfo(id=id, title=title, synopsis=synopsis,
                                    rating=rating, episodes=None))
        return animes
    
    def __processEpisodesInfo(self, elements:ResultSet) -> List[EpisodeInfo]:
        """
        Process the resultSet and returns the list with the episodes.
        
        :param ResultSet elements:
            Result of elements get by query.
        """
        episodes = []

        return episodes
    # ----

    # ---- PUBLIC METHODS ----
    def Search(self, animeName:str) -> List[AnimeInfo]:
        
        params = dict()

        if animeName is not None:
            params["q"] = animeName

        params = urlencode(params)

        url = f"{self.__browseUrl}"
        if params:
            url += f"?{params}"

        response = self.__scrapper.get(url=url)
        soup = BeautifulSoup(response.text, features="html.parser")
        
        elements = soup.select("div.Container ul.ListAnimes li article")

        return self.__processAnimesInfo(elements=elements)