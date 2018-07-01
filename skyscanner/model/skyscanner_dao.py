from pymongo import MongoClient
from model.skyscanner_airport import SkyscannerAirport


class SkyscannerDAO:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.skyscanner
        self.collection = self.db.airports
        self.journey_collection = self.db.journey

    def get_country_airports(self, country_name):
        result = self.collection.find({"country": country_name})
        out_airports = list()
        for row in result:
            airport = SkyscannerAirport(row["country"], row["city"], row["code"], row["name"])
            out_airports.append(airport)
        return out_airports

    def get_price_for_ticket(self, day, month, year, ori, dest):
        result = self.journey_collection.find_one({
            "ori": ori,
            "dest": dest,
            "month": month,
            "day": day,
            "year": year
        })
        price = -1
        if result is not None:
            price = result["price"]
        else:
            print("Entry not found!!")
        return price

    def get_combination_price(self, combination, day_range):

        first_day = day_range[0]
        return True
        # tiene que devolver un mapeo del precio de cada dia para esa combinacion
