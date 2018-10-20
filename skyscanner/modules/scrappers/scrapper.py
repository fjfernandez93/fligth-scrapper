from abc import ABC, abstractmethod
from pymongo import MongoClient
import time

from common.flags import GlobalState


class Scrapper(ABC):

    def __init__(self, site):
        self.site = site

    def store_info_journey(self, scrap_data, day, price):

        client = MongoClient()
        collection = client.skyscanner.journey
        data = {
            "ori": scrap_data.ori,
            "dest": scrap_data.dest,
            "month": scrap_data.month,
            "year": scrap_data.year,
            "day": day,
            "price": price,
            "queryDate": time.time(),
            "site": self.site
        }
        collection.insert_one(data).inserted_id
        client.close()

    @abstractmethod
    def do_scrapping(self, scrap_data):
        """
        Main method called to start the scrapping process.
        :param ryanair_scrap_data: RyanairScrapData with the query info.
        :return: None
        """
        pass

    def start_scrapping(self, scrap_data):
        while not GlobalState.can_start_scrapper():
            time.sleep(1)
        self.do_scrapping(scrap_data)
