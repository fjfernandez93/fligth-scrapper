from model.skyscanner_dao import SkyscannerDAO
import model.skyscanner_trip
import datetime

dao = SkyscannerDAO()


def generate_combinations(ori, dest):
    """
    Generate the possible combinations between airports of two given countries.
    :param ori: origin country
    :param dest: destination country
    :return: a list with all the combinations
    """
    airports_ori = dao.get_country_airports(ori)
    airports_dest = dao.get_country_airports(dest)

    ori_to_dest = list()
    dest_to_ori = list()
    combinations = list()

    for ap_o in airports_ori:
        for ap_d in airports_dest:
            ori_to_dest.append((ap_o.code, ap_d.code))
            dest_to_ori.append((ap_d.code, ap_o.code))

    for jrny_o in ori_to_dest:
        for jrny_d in dest_to_ori:
            combi = dict()
            combi["to"] = jrny_o
            combi["from"] = jrny_d
            combinations.append(combi)

    return combinations


def filter_combinations(combinations, mode):
    """
    Filter a list of combinations, extracting only those which satisfy the condition of filter mode.
    :param combinations: a list with all the combinations to filter
    :param mode: the filter mode
    :return: a list of the filtered combinations.
    """
    filtered_combinations = list()

    # Mode 1: same airport in origin country.
    if mode == 1:
        [filtered_combinations.append(x) for x in combinations if x["to"][0] == x["from"][1]]
    # Mode 2: same airport in destination country.
    elif mode == 2:
        [filtered_combinations.append(x) for x in combinations if x["to"][1] == x["from"][0]]
    # Mode 3: same airport in both destination and origin country.
    elif mode == 3:
        [filtered_combinations.append(x) for x in combinations if x["to"][0] == x["from"][1] and x["to"][1] == x["from"][0]]
    # No filter.
    else:
        filtered_combinations = combinations
    return filtered_combinations


def get_day_ranges(first, last, length):
    """
    Method to obtain all the days ranges of a given length inside a date.
    :param first: first day of the date
    :param last: last day of the date
    :param length: length of the ranges
    :return: a list of tuples. Each tuple contains the first an last day of a range.
    """
    delta_time = datetime.timedelta(days=length-1)
    delta_time_one = datetime.timedelta(days=1)

    days_list = list()
    current = first

    while current <= last - delta_time:
        range_days = list()
        day_trip = current
        end = current + delta_time

        while day_trip <= end:
            range_days.append(day_trip)
            day_trip = day_trip + delta_time_one

        days_list.append(range_days)
        current = current + delta_time_one

    return days_list


def get_trip_list(sky_query):
    """
    Main method to obtain all the possible combinations for a given query.
    :param sky_query: The object containing the information of thw query.
    :return: a list with all the Trip objects (all the possible combination)
    """
    # Create all the combinations and filter it by the condition given in the Skyquery object
    airport_combis = generate_combinations(sky_query.ori, sky_query.dest)
    airport_combis = filter_combinations(airport_combis, sky_query.filter_mode)

    # Get all the possible day ranges between the dates of the query, given by the length of the query.
    day_ranges = get_day_ranges(sky_query.first_day, sky_query.last_day, sky_query.length)

    result = list()
    for combi in airport_combis:
        for rang in day_ranges:
            # Create trip object and assign prices from database
            trip_obj = model.skyscanner_trip.SkyscannerTrip(combi["to"], combi["from"], rang[0], rang[-1])
            trip_obj.set_price()
            result.append(trip_obj)

    # Remove trips with ticket with -1 price (no have tickets available).
    to_remove = list()
    for res in result:
        if res.ori_price == 0 or res.dest_price == 0:
            to_remove.append(res)
    for tr in to_remove:
        result.remove(tr)

    return result
