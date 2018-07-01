from selenium import webdriver
from bs4 import BeautifulSoup
import re
from time import sleep
import sys
from pymongo import MongoClient
import time


url_base = "https://www.skyscanner.es/transporte/vuelos/{}/{}/?adults={}&children=0&a\
dultsv2={}&childrenv2&infants=0&cabinclass=economy&rtn=0&preferdirects=false\
&outboundaltsenabled=false&inboundaltsenabled=false&oym={}&ref=home&selectedoday=01"


def store_info_journey(ori, dest, adults, year, month, price, day, now):

    client = MongoClient()
    collection = client.skyscanner.journey
    data = {
        "ori" : ori,
        "dest" : dest,
        "month" : month,
        "year" : year,
        "day": day,
        "price": price,
        "queryDate": now
    }
    collection.insert_one(data).inserted_id
    client.close()


def get_and_store_info_from_web(airport1, airport2, num_adults, year, month):

    year_aux = "%02d" % year
    month_aux = "%02d" % month
    date = year_aux + month_aux

    # --- OBTAIN HTML DATA ---

    url_for = url_base.format(airport1, airport2, num_adults, num_adults, date)
    driver = webdriver.Firefox()
    driver.get(url_for)
    sleep(10)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    # --- EXTRACT PRICES ---

    # Find cells with the prices
    days = soup.find_all("button", {"class":re.compile("month-view-calendar__cell") })
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
    now = time.time()
    for i in range(1,len(prices)+1):
        store_info_journey(airport1, airport2, num_adults, year, month, prices[i - 1], i, now)

    driver.close()


if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage: python testSky.py ori dest adults year month")
        print("Example: python testSky.py mad krk 2 18 9")
    else:
        airport_ori = sys.argv[1]
        airport_dest = sys.argv[2]
        num_adults = sys.argv[3]
        year = int(sys.argv[4])
        month = int(sys.argv[5])
        get_and_store_info_from_web(airport_ori, airport_dest, num_adults, year, month)

