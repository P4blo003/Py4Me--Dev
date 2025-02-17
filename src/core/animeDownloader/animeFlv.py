# ---- MODULES ----
import requests
from bs4 import BeautifulSoup

from typing import List
from dataclasses import dataclass

from src.utils.file import LoadFromJSON
# ---- CLASSES ----
@dataclass
class AnimeInfo:
    """
    Keeps basic data of an anime.
    """
    title:str
    queryUrl:str
    animeType:str

class AnimeFlv:
    """
    Default interface to manage anime querys to AnimeFlv web.
    """
    # ---- DEFAULT METHODS ----
    def __init__(self):
        """
        Empty constructor. Initializes the class properties.
        """
        data = LoadFromJSON('/home/pablo/Projects/Py4Me/src/core/animeDownloader/manifest.json')

        self.__webURl = data.get('WEB_URL')
        self.__queryUrl = f"{self.webUrl}/{data.get('QUERY_URL')}"

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

    # ---- PRIVATE METHODS ----
    def __generateSearcURl__(self,anime:str) -> str:
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
    def LookFor(self, name:str) -> List[AnimeInfo]:
        """
        Look for a given anime and return the results.

        :param str name:
            Anime name.
        """

        animes = []     # To keep the obtained animes.

        url = self.__generateSearcURl__(name)   # Generates the Url.

        response = requests.get(url=url)        # Make the request.

        if response.status_code == 200:         # If the request was OK.
            html = BeautifulSoup(response.text, "html.parser")  # Obtain the HTML.

            animeList = html.select("div.Container ul.ListAnimes li")   # Get the <li> label from the Html
                                                                        # where the animes are.

            for animeData in animeList:     # For each anime.
                
                # Gets the general data.
                title = animeData.find('h3', class_="Title").string
                queryUrl = animeData.find('a')["href"]
                animeType = animeData.find('span', class_="Type").string

                animes.append(AnimeInfo(title=title, queryUrl=queryUrl, animeType=animeType))   # Keeps the data into the list.

        else:
            print("BAD")

        return animes   # Returns the list.
        
# ----