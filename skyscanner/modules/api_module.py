from modules.ryanair_scrapper import RyanairScrapper
from modules.skyscanner_scrapper import SkyscannerScrapper
import modules.combinations_module
import threading
from model.skyscanner_dao import SkyscannerDAO
from model.scrapping_model import RyanairScrapData, SkyscannerScrapData


def scrap_trip_in_site(site, ori, dest, year, month):

    process = None
    if site == 'ryanair':
        obj = RyanairScrapData(ori, dest, 2, year, month)
        scrp = RyanairScrapper()
        process = threading.Thread(target=scrp.start_scrapping, args=(obj,))
    elif site == 'skyscanner':
        obj = SkyscannerScrapData(ori, dest, 2, year, month)
        scrp = SkyscannerScrapper()
        process = threading.Thread(target=scrp.start_scrapping, args=(obj,))

    if process is not None:
        process.start()
    else:
        # TODO: raise a custom exception
        pass


def scrap_combination_in_site(site, ori, dest, year, month):
    combinations = modules.combinations_module.generate_airport_combinations(ori, dest)
    for comb in combinations:
        scrap_trip_in_site(site, comb[0], comb[1], year, month)


def search_data(ss_query):
    """
    Method to manage the logic when a client query is done. It checks if there is valid data
    to return. If it's not found, then scrap it.
    :param sky_query: SkyscannerQuery object with the query data
    :return: the found data (may be empty)
    """
    output = list()
    # Check if it exists valid data
    dao = SkyscannerDAO()

    if dao.check_valid_query_data(ss_query):
        # If a valid query already exists, get and return the data.
        raw_combs = modules.combinations_module.get_trip_list(ss_query)
        ordered_combs = sorted(raw_combs, key=lambda trip: trip.total_price)
        for trip in ordered_combs:
            output.append({
                "trip1": str(trip.ori_combi),
                "day1": str(trip.ori_date),
                "site1": str(trip.ori_site),
                "trip2": str(trip.dest_combi),
                "day2": str(trip.dest_date),
                "site2": str(trip.dest_site),
                "price": trip.total_price
            })
    else:
        # If no valid query exists, scrap the data with a thread per site and store the query info.
        print("No data found!!")
        dao.insert_query_data(ss_query)
        # TODO: get from config
        sites = ["ryanair", "skyscanner"]
        for site in sites:
            scrap_combination_in_site(site, ss_query.ori, ss_query.dest, ss_query.first_day.year, ss_query.first_day.month)
        output.append({
            "trip1": "No data",
            "day1": "No data",
            "trip2": "No data",
            "day2": "No data",
            "price": "No data"
        })
    return output
