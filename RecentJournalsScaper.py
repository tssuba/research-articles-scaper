import sys
import pprint
import json
import pandas as pd
import requests
import os

from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict, Union

load_dotenv()

ResearchArticle = Dict[str, Union[str, datetime]]

class RecentJournalsScraper:

    # Constants
    DATE_TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
    BASE_URL_SCOPUS = "http://api.elsevier.com/content/search/scopus?query=%28net+zero+carbon%29&field=citedby-count,title,prism:doi,prism:coverDate,prism:publicationName"
    API_KEY_SCOPUS = os.getenv('API_KEY_SCOPUS')
    INST_TOKEN_SCOPUS = os.getenv('INST_TOKEN_SCOPUS')

    def __init__(self):
        
        self.urlScopus = (f"{self.BASE_URL_SCOPUS}&apiKey={self.API_KEY_SCOPUS}&insttoken={self.INST_TOKEN_SCOPUS}")

        self.pretty_printer = pprint.PrettyPrinter()
    

    def parse_string_to_datetime(self, date_time_str: str) -> datetime:
        """
        Method parses string to python datetime object.

        Args:
            date_time_str (str): Datetime string.

        Returns:
            date_time_obj (datetime): Parsed python datetime object.
        """

        date_time_obj = datetime.strptime(date_time_str, self.DATE_TIME_FORMAT)
        return date_time_obj
    

    def scrape_scopus(self) -> List[ResearchArticle]:

        id = self.urlScopus
        articles: List[ResearchArticle] = []
        headersid={'Accept': 'application/json', 'field':'description'}
        responseid = requests.get(id,headers=headersid)
        sid=responseid.content.decode("utf-8")
        contid=json.loads(sid) 
        contid
        box=pd.DataFrame(contid['search-results']['entry'])[['dc:title','prism:doi', 'prism:coverDate','prism:publicationName']]
        articles = box.to_dict('records')
        return articles
    

    def print_articles(self, articles: List[ResearchArticle]):
        """
        Method pretty prints scraped articles.

        Args:
            articles (List[GoogleNewsArticle]): Scraped Articles.
        """

        self.pretty_printer.pprint(articles)


if __name__ == "__main__":

    research_scaper = RecentJournalsScraper()

    articles = research_scaper.scrape_scopus()

    research_scaper.print_articles(articles)