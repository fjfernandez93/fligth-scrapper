from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import re
from time import sleep
import datetime

import common.tools
from common.flags import GlobalState
from modules.scrappers.scrapper import Scrapper


class RyanairScrapper(Scrapper):

    def __init__(self):
        super().__init__("ryanair")
        self.url_base = "https://www.ryanair.com/es/es/booking/home/{}/{}/{}//{}/0/0/0"
        self.result = dict()
        self.months = ["Ene.", "Feb.", "Mar.", "Abr.", "May.", "Jun.", "Jul.", "Ago.", "Sep.", "Oct.", "Nov.", "Dic."]

    def parse_date(self, date, year):
        """
        Helper for parse the extracted date into a python date
        :param date: date extracted from the website
        :return: datetime.date formatted
        """
        split_date = date.split(" ")
        day = split_date[1]
        month = self.months.index(split_date[2])
        date = datetime.date(year, int(month)+1, int(day))
        return date

    def iterative_scrapper(self, driver, month, year):
        """
        Method for extract the prices that appears in a Ryanair query. It extracts more than it's visible.

        :param driver: browser driver
        :param month: month of the query, to avoid to extarct those which doesn't belong to the query
        :return: None
        """

        html = driver.page_source
        # First I use a pre-process to extract the main section where the prices are, because using directly BS in the
        # page source is does not work.
        main_text = re.findall(r'(<div class="body-section(.*)<div class="clearfix"></div>)', html)[0][0]
        soup = BeautifulSoup(main_text, "html.parser")

        # Each slide represents a day
        slides = soup.findAll("div", {"class": "slide"})
        for slide in slides:
            date = slide.find("div", {"class": "date"}).get_text()
            try:
                date = self.parse_date(date, year)
                # Avoid the days of other months.
                if date.month == month:
                    info = slide.find("div", {"class": "fare"}).get_text().replace(u'\xa0', ' ').split(" ")
                    price = float(info[0].replace(',', '.'))
                    currency = info[1]
                    price = float(price)
                    if currency != "€":
                        # Currency to euro.
                        price = common.tools.parse_currency_to_eur(price, currency)
                    # Because the hidden slides may have an unreal price of 0, if they are already scrapped but
                    # the scrapped value is greater than 0, overwrite it.
                    if date not in self.result.keys() or price > 0:
                        self.result[date] = price
            except ValueError:
                continue

    def do_scrapping(self, ryanair_scrap_data):

        # Format the url with the data received.
        url_for = self.url_base.format(ryanair_scrap_data.ori.upper(), ryanair_scrap_data.dest.upper(),
                                       ryanair_scrap_data.date, ryanair_scrap_data.adults)
        driver = webdriver.Firefox()
        driver.get(url_for)
        sleep(10)

        # Do the first scrap
        self.iterative_scrapper(driver, ryanair_scrap_data.month, ryanair_scrap_data.year)
        for i in range(0, 6):
            # Find and press the button to show the next 5 days, scrap them and repeat
            wait = WebDriverWait(driver, 10)
            button = wait.until(ec.visibility_of_element_located((By.XPATH, "//button[@class='arrow left']")))
            # button = driver.find_element_by_xpath("//button[@class='arrow left']")
            button.click()
            sleep(10)
            self.iterative_scrapper(driver, ryanair_scrap_data.month, ryanair_scrap_data.year)

        # Store the results after order them
        for k in sorted(self.result.keys()):
            self.store_info_journey(ryanair_scrap_data, k.day, self.result[k])

        # Close the browser
        driver.close()
        self.result.clear()
        GlobalState.finished_scrapper()

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
#         r = RyanairScrapper()
#         data = RyanairScrapData(airport_ori, airport_dest, num_adults, year, month)
#         r.scrap_ryanair(data)

