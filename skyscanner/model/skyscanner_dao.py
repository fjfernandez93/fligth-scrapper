import time
from pymongo import MongoClient
from model.skyscanner_airport import SkyscannerAirport
import datetime


class SkyscannerDAO:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.skyscanner
        self.collection = self.db.airports
        self.journey_collection = self.db.journey
        self.query_collection = self.db.query

    def get_country_airports(self, country_name):
        """
        Get all the airports for a given country
        :param country_name: the country name
        :return: a list of SkyscannerAirport objects
        """
        result = self.collection.find({"country": country_name})
        out_airports = list()
        for row in result:
            airport = SkyscannerAirport(row["country"], row["city"], row["code"], row["name"])
            out_airports.append(airport)
        return out_airports

    def get_price_for_ticket(self, day, month, year, ori, dest):
        price = 0
        site = ""
        result = self.journey_collection.find({
            "ori": ori,
            "dest": dest,
            "month": month,
            "day": day,
            "year": year
        })
        if result is not None:
            price = 9999999
            for res in result:
                if res["price"] < price:
                    price = res["price"]
                    site = res["site"]
        else:
            print("Entry not found!!")
        if price == 9999999:
            price = 0
        return (price, site)

    def check_valid_query_data(self, ss_query):
        """
        Check if it exists valid data to answer a query
        :param ss_query: SkyscannerQuery object with the query data
        :return: bool
        """

        # Limit timestamp: now minus 2 weeks (in seconds)
        # TODO: extract it from config file
        limit = time.time() - 1209600

        result = self.query_collection.find_one({
            "ori": ss_query.ori,
            "dest": ss_query.dest,
            "length": ss_query.length,
            "first_day": datetime.datetime.combine(ss_query.first_day, datetime.time.min),
            "last_day":  datetime.datetime.combine(ss_query.last_day, datetime.time.min),
            "timestamp": {"$gt": limit}
        })
        return result is not None

    def insert_query_data(self, ss_query):

        self.query_collection.insert({
            "ori": ss_query.ori,
            "dest": ss_query.dest,
            "length": ss_query.length,
            "first_day": datetime.datetime.combine(ss_query.first_day, datetime.time.min),
            "last_day": datetime.datetime.combine(ss_query.last_day, datetime.time.min),
            "timestamp": ss_query.timestamp
        })
