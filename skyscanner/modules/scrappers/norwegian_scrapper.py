from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from common.flags import GlobalState
from modules.scrappers.scrapper import Scrapper


class NorwegianScrapper(Scrapper):

    def __init__(self):
        super().__init__("norwegian")
        self.url_base = "https://www.norwegian.com/es/reserva/reserve-su-vuelo/precios-baratos/?A_City={}" \
                        "&AdultCount=1&ChildCount=0&CurrencyCode=EUR&D_City={}&D_Day=02&D_Month={}" \
                        "&D_SelectedDay=02&IncludeTransit=true&InfantCount=0&R_Day=18&R_Month={}&TripType=1" \
                        "&mode=ab#/?origin={}&destination={}&outbound={}&adults=1&oneWay=true&currency=EUR"

    def do_scrapping(self, norweigan_scrap_data):

        # --- OBTAIN HTML DATA ---
        month_aux = month_aux = "%02d" % norweigan_scrap_data.month
        date = "{}{}".format(norweigan_scrap_data.year, month_aux)
        date2 = "{}-{}".format(norweigan_scrap_data.year, month_aux)
        url_for = self.url_base.format(norweigan_scrap_data.dest, norweigan_scrap_data.ori, date, date,
                                       norweigan_scrap_data.ori, norweigan_scrap_data.dest, date2)
        driver = webdriver.Firefox()
        driver.get(url_for)
        sleep(10)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        calendar = soup.find("div", {"class": "lowfare-calendar-combo__content"})
        if calendar is not None:

            # --- EXTRACT PRICES ---
            prices = list()
            list_row = soup.findAll("tr", {"class": "lowfare-calendar__row lowfare-calendar__row--animate"})

            for tr in list_row:
                list_td = tr.findAll("td", {"class": "lowfare-calendar__cell"})
                for td in list_td:
                    dummy_list = td.findAll("div", {"class": "lowfare-calendar__item--dummy"})

                    if len(dummy_list) == 0:
                        button = td.button
                        # Get day
                        span = button.find("span", {"class": "lowfare-calendar__date"})
                        day = span.get_text().replace(".", "")

                        price = 0
                        not_empty = "lowfare-calendar__item--empty" not in button["class"]
                        if not_empty:
                            price_element = button.find("strong", {"class": "lowfare-calendar__price"})
                            if price_element is not None:
                                price_text = price_element.get_text().strip().replace(".", "").replace(",", ".")
                                price = float(price_text)
                        prices.append(price)

            # --- STORE INFO ---

            for i in range(1, len(prices)+1):
                self.store_info_journey(norweigan_scrap_data, i, prices[i - 1])

        driver.close()
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
    #         month = int(sys.argv[5])
    #         skyscanner_scrap_data = SkyscannerScrapData(airport_ori, airport_dest, num_adults, year, month)
    #         scrap_skyscanner(skyscanner_scrap_data)

