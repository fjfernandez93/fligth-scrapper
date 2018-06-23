from model.skyscanner_dao import SkyscannerDAO
import datetime

dao = SkyscannerDAO()


def generate_combinations(ori, dest):
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

    filtered_combinations = list()

    if mode == 1:
        [filtered_combinations.append(x) for x in combinations if x["to"][0] == x["from"][1]]
    elif mode == 2:
        [filtered_combinations.append(x) for x in combinations if x["to"][1] == x["from"][0]]
    elif mode == 3:
        [filtered_combinations.append(x) for x in combinations if x["to"][0] == x["from"][1] and x["to"][1] == x["from"][0]  ]
    return filtered_combinations


def get_day_ranges(first, last, length):

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
