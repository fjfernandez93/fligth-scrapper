from pymongo import MongoClient
from model.skyscanner_airport import SkyscannerAirport


class SkyscannerDAO:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.skyscanner
        self.collection = self.db.airports

    def get_country_airports(self, country_name):
        result = self.collection.find({"country": country_name})
        out_airports = list()
        for row in result:
            airport = SkyscannerAirport(row["country"], row["city"], row["code"], row["name"])
            out_airports.append(airport)
        return out_airports