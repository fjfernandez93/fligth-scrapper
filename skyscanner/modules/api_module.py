from modules.ryanair_scrapper import RyanairScrapper
from modules.skyscanner_scrapper import SkyscannerScrapper
import modules.combinations_module
import threading
from model.scrapping_model import RyanairScrapData, SkyscannerScrapData


def scrap_site(site, ori, dest, year, month):

    if site == 'ryanair':
        obj = RyanairScrapData(ori, dest, 2, year, month)
        scrp = RyanairScrapper()
        process = threading.Thread(target=scrp.do_scrapping, args=(obj,))
    elif site == 'skyscanner':
        obj = SkyscannerScrapData(ori, dest, 2, year, month)
        scrp = SkyscannerScrapper()
        process = threading.Thread(target=scrp.scrap_skyscanner, args=(obj,))

    process.start()


def search_data(sky_query):
    raw_combs = modules.combinations_module.get_trip_list(sky_query)
    ordered_combs = sorted(raw_combs, key=lambda trip: trip.total_price)

    output = list()
    for trip in ordered_combs:
        output.append({
            "trip1": str(trip.ori_combi),
            "day1": str(trip.ori_date),
            "trip2": str(trip.dest_combi),
            "day2": str(trip.dest_date),
            "price": trip.total_price,

        })
    return output
