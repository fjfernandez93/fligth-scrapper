from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
from pymongo import MongoClient
import time
from model.scrapping_model import SkyscannerScrapData


class SkyscannerScrapper:

    def __init__(self):
        self.url_base = "https://www.skyscanner.es/transporte/vuelos/{}/{}/?adults={}&children=0&a\
                        dultsv2={}&childrenv2&infants=0&cabinclass=economy&rtn=0&preferdirects=false\
                        &outboundaltsenabled=false&inboundaltsenabled=false&oym={}&ref=home&selectedoday=01"

    def store_info_journey(self, skyscanner_scrap_data, price, day):
        """
        Store in mongoDB the information about trip day
        :param skyscanner_scrap_data: The object containing information about the query
        :param price: the price of the day
        :param day: the number of the day
        :return: None
        """
        client = MongoClient()
        collection = client.skyscanner.journey
        data = {
            "ori" : skyscanner_scrap_data.ori,
            "dest" : skyscanner_scrap_data.dest,
            "month" : skyscanner_scrap_data.month,
            "year" : skyscanner_scrap_data.year,
            "day": day,
            "price": price,
            "queryDate": time.time(),
            "site": 'sky_scanner'
        }
        id = collection.insert_one(data).inserted_id
        client.close()

    def scrap_skyscanner(self, skyscanner_scrap_data):
        """
        Scrap the prices of a given month in Sky Scanner, and store them
        in database.

        :param airport1: Origin airport
        :param airport2: Destination airport
        :param num_adults: nº of adults
        :param year: date -> year
        :param month: date -> month
        :return:
        """

        # --- OBTAIN HTML DATA ---

        url_for = self.url_base.format(skyscanner_scrap_data.ori, skyscanner_scrap_data.dest,
                                       skyscanner_scrap_data.adults, skyscanner_scrap_data.adults, skyscanner_scrap_data.date)
        driver = webdriver.Firefox()
        driver.get(url_for)
        sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # --- EXTRACT PRICES ---

        # Find cells with the prices
        days = soup.find_all("button", {"class":re.compile("month-view-calendar__cell")})
        prices = []

        # Filter days of the month searched
        for day in days:
            if "month-view-calendar__cell--outside" not in day.attrs["class"]:
                descendants = day.find_all()
                # Only available prices
                if len(descendants) == 2:
                    price = int((descendants[1].text[0:-2]).replace(".",""))
                    prices.append(price)
                # If price is not available, set it to -1
                else:
                    prices.append(-1)

        # --- STORE INFO ---

        for i in range(1, len(prices)+1):
            self.store_info_journey(skyscanner_scrap_data, prices[i - 1], i)

        driver.close()


    # if __name__ == "__main__":
    #
    #     if len(sys.argv) != 6:
    #         print("Usage: python testSky.py ori dest adults year month")
    #         print("Example: python testSky.py mad krk 2 18 9")
    #     else:
    #         airport_ori = sys.argv[1]
    #         airport_dest = sys.argv[2]
    #         num_adults = sys.argv[3]
    #         year = int(sys.argv[4])
    #         month = int(sys.argv[5])
    #         skyscanner_scrap_data = SkyscannerScrapData(airport_ori, airport_dest, num_adults, year, month)
    #         scrap_skyscanner(skyscanner_scrap_data)

