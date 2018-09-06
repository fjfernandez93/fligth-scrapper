from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
import sys
from pymongo import MongoClient
import time
import datetime
import calendar

from model.scrapping_model import RyanairScrapData
import common.tools

class RyanairScrapper:

    def __init__(self):

        self.url_base = "https://www.ryanair.com/es/es/booking/home/{}/{}/{}//{}/0/0/0"
        self.result = dict()
        self.months = ["Ene.", "Feb.", "Mar.", "Abr.", "May.", "Jun.", "Jul.", "Ago.", "Sep.", "Oct.", "Nov.", "Dic."]

    def store_info_journey(self, ryanair_scrap_data, date, price):

        client = MongoClient()
        collection = client.skyscanner.journey
        data = {
            "ori" : ryanair_scrap_data.ori,
            "dest" : ryanair_scrap_data.dest,
            "month" : date.month,
            "year" : date.year,
            "day": date.day,
            "price": price,
            "queryDate": time.time(),
            "site": 'ryanair'
        }
        collection.insert_one(data).inserted_id
        client.close()


    def parse_date(self, date):
        split_date = date.split(" ")
        day = split_date[1]
        month = self.months.index(split_date[2])
        date = datetime.date(2018, int(month)+1, int(day))
        return date

    def iterative_crawler(self, driver):

        html = driver.page_source
        main_text = re.findall(r'(<div class="body-section(.*)<div class="clearfix"><\/div>)', html)[0][0]
        soup = BeautifulSoup(main_text, "html.parser")

        # --- EXTRACT PRICES ---

        slides = soup.findAll("div", {"class": "slide"})
        for slide in slides:
            date = slide.find("div", {"class": "date"}).get_text()
            try:
                date = self.parse_date(date)
                info = slide.find("div", {"class": "fare"}).get_text().replace(u'\xa0', ' ').split(" ")
                price = float(info[0].replace(',', '.'))
                currency = info[1]
                price = float(price)
                if currency != "€":
                    price = common.tools.parse_currency_to_eur(price, currency)
                if date not in self.result.keys() or price > 0:
                    self.result[date] = price
            except ValueError:
                continue

    def scrap_ryanair(self, ryanair_scrap_data):

        # --- OBTAIN HTML DATA ---

        url_for = self.url_base.format(ryanair_scrap_data.ori.upper(), ryanair_scrap_data.dest.upper(),
                                       ryanair_scrap_data.date, ryanair_scrap_data.adults)
        driver = webdriver.Firefox()
        driver.get(url_for)
        sleep(10)

        self.iterative_crawler(driver)
        for i in range(0, 6):
            button = driver.find_element_by_xpath("//button[@class='arrow left']")
            button.click()
            sleep(4)
            self.iterative_crawler(driver)

        for k in sorted(self.result.keys()):
            self.store_info_journey(ryanair_scrap_data, k, self.result[k])
        driver.close()
        self.result.clear()


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
#         month = sys.argv[5]
#
#         data = RyanairScrapData(airport_ori, airport_dest, num_adults, year, month)
#         scrap_ryanair(data)

