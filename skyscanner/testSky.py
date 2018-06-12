from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re
from time import sleep
import sys
from pymongo import MongoClient
import time


url_base = "https://www.skyscanner.es/transporte/vuelos/{}/{}/?adults={}&children=0&a\
dultsv2={}&childrenv2&infants=0&cabinclass=economy&rtn=0&preferdirects=false\
&outboundaltsenabled=false&inboundaltsenabled=false&oym={}&ref=home&selectedoday=01"

def storeInfoJourney(ori,dest,adults,year,month,price,day):

    client = MongoClient()
    collection = client.skyscanner.journey
    data = {
        "ori" : ori,
        "dest" : dest,
        "timestamp" : time.time(),
        "month" : month,
        "year" : year,
        "day": day,
        "price": price
    }
    collection.insert_one(data).inserted_id
    client.close()

def getAndStoreInfoFromWeb(airport1, airport2, num_adults, year, month):

    year_aux = "%02d" % (year)
    month_aux = "%02d" % (month)
    date = year_aux + month_aux

    # OBTAIN HTML DATA

    url_for = url_base.format(airport1,airport2,num_adults,num_adults,date)
    driver = webdriver.Firefox()
    driver.get(url_for)
    sleep(10)
    html = driver.page_source

    #shtml = open("test.html","r")
    soup = BeautifulSoup(html, "html.parser")

    #### EXTRACT PRICES ####

    # Find cells with the prices
    days = soup.find_all("button", {"class":re.compile("month-view-calendar__cell") })
    prices = []

    # Filter days of the month searched
    for day in days:
        if "month-view-calendar__cell--outside" not in day.attrs["class"]:
            descendats = day.find_all()   
            # Only prices availables        
            if len(descendats) == 2:
                price = int(descendats[1].text[0:-2])
                prices.append(price)
            # If price is not available, set it to -1
            else:
                prices.append(-1)

    #### STORE INFO ####

    for i in range(1,len(prices)+1):
        #storeInfoJourney(airport1,airport2,num_adults,year,month,prices[i-1],i) 
        print(prices[i])
    #driver.close()



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
        getAndStoreInfoFromWeb(airport_ori, airport_dest, num_adults, year, month)

