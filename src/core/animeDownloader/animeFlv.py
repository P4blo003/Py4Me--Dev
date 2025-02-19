# ---- MODULES ----
import requests
from bs4 import BeautifulSoup

from typing import Optional, List
from dataclasses import dataclass

from src.utils.file import LoadFromJSON
# ---- CLASSES ----
@dataclass
class Episode:
    """
    Keeps basic data of an episode.
    """

    title:str
    queryUrl:Optional[List[str]] = None
    
class Anime:
    """
    Keeps basic data of an anime.
    """
    # ---- DEFAULT METHODS ----
    def __init__(self, title:str, description:str, rating:str, queryUrl:str, animeType:str):
        """
        Param constructor. Initializes the class properties.
        """
        self.__title:str = title
        self.__description:str = description
        self.__rating:str = rating
        self.__queryUrl:str = queryUrl
        self.__animeType:str = animeType
        self.__episodes: Optional[List[Episode]] = None
    
    def __repr__(self):
        """
        Returns the string format of the object.
        """
        return f"Title:{self.title} | Rating: {self.rating} | Type: {self.animeType}"

    # ---- PROPERTIES ----
    @property
    def title(self) -> str:
        """
        Returns the anime title.
        """
        return self.__title
    @property
    def description(self) -> str:
        """
        Returns the anime description.
        """
        return self.__description
    @property
    def rating(self) -> str:
        """
        Returns the anime rating.
        """
        return self.__rating
    @property
    def queryUrl(self) -> str:
        """
        Returns the anime query url.
        """
        return self.__queryUrl
    @property
    def animeType(self) -> str:
        """
        Returns the anime title.
        """
        return self.__animeType
    @property
    def episodes(self) -> List[Episode]:
        """
        Returns the anime episodes list.
        """
        if not self.__episodes:
            self.FindEpisodes()
        return self.__episodes

    # ---- METHODS ----
    def FindEpisodes(self):
        """
        Find the episodes of the anime.
        """
        pass

class AnimeFlv:
    """
    Default interface to manage anime querys to AnimeFlv web.
    """
    # ---- DEFAULT METHODS ----
    def __init__(self, animeToSearch:str):
        """
        Empty constructor. Initializes the class properties.
        """

        data = LoadFromJSON('/home/pablo/Projects/Py4Me/src/core/animeDownloader/manifest.json')

        self.__webURl:str = data.get('WEB_URL')
        self.__queryUrl:str = data.get('QUERY_URL')

        self.__animes:Optional[List[Anime]] = []

        self.FindAnimes(animeToSearch)
    
    def __repr__(self):
        """
        Returns the string format of the object.
        """
        return f"AnimeFlv | Animes: {len(self.animes)}"

    # ---- PROPERTIES ----
    @property
    def webUrl(self) -> str:
        """
        Returns the web url.
        """

        return self.__webURl
    
    @property
    def queryURl(self) -> str:
        """
        Returns the query url.
        """

        return self.__queryUrl
    
    @property
    def animes(self) -> List[Anime]:
        """
        Returns the animes.
        """

        return self.__animes

    # ---- PRIVATE METHODS ----
    def __generateSearcURl(self,anime:str) -> str:
        """
        Generates the query url for the given anime name.

        :param str anime:
            Anime name.
        """
        params = anime.split(" ")   # This is because the query can be "Dragon Ball" and we should
                                    # adjust the query.
        q = params[0]               # The query initialy is "Dragon".
        
        if len(params) > 1:         # If there are more params (The query had spaces: "Dragon Ball")
            for value in params[1:]:    # For each param.
                q += f"+{value}"         # Append like: Dragon+Ball+...

        return f"{self.queryURl}{q}"    # The final query is "...q=Dragon+Ball+..."

    # ---- PUBLIC METHODS ----
    def FindAnimes(self, name:str):
        """
        Look for a given anime and return the results.

        :param str name:
            Anime name.
        """

        self.__animes = []     # To keep the obtained animes.

        url = self.__generateSearcURl(name)   # Generates the Url.

        response = requests.get(url=url)        # Make the request.

        if response.status_code == 200:         # If the request was OK.
            html = BeautifulSoup(response.text, "html.parser")  # Obtain the HTML.

            animeList = html.select("div.Container ul.ListAnimes li")   # Get the <li> label from the Html
                                                                        # where the animes are.
            for animeData in animeList:     # For each anime.
                
                # Gets the general data.
                title = animeData.find('h3', class_="Title").string
                description = animeData.find_all('p')[1].string
                rating = animeData.find('span', class_="Vts").string
                queryUrl = animeData.find('a')["href"]
                animeType = animeData.find('span', class_="Type").string

                self.__animes.append(Anime(title=title, description=description, rating=rating, 
                                        queryUrl=queryUrl, animeType=animeType))   # Keeps the data into the list.
    
    def GetAnimeAt(self, index:int) -> Anime:
        """
        Returns the anime at the given index.
        """
        
        if index < 0 or index > len(self.animes):
            return
        
        if not self.animes:
            return
        
        return self.animes[index]
# ----