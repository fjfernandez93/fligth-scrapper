from pymongo import MongoClient
from model.skyscanner_airport import SkyscannerAirport


class SkyscannerDAO:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.skyscanner
        self.collection = self.db.airports
        self.journey_collection = self.db.journey

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
        else:
            print("Entry not found!!")
        if price == 9999999:
            price = 0
        return price

    def get_combination_price(self, combination, day_range):

        first_day = day_range[0]
        return True
        # tiene que devolver un mapeo del precio de cada dia para esa combinacion
