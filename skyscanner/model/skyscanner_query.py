import time

class SkyscannerQuery:

    def __init__(self, ori, dest, length, first_day, last_day, filter_mode):
        self.ori = ori
        self.dest = dest
        self.length = length
        self.first_day = first_day
        self.last_day = last_day
        self.filter_mode = filter_mode
        self.trip_list = list()
        self.timestamp = time.time()

    @property
    def trip_list_by_price(self):
        return sorted(self.trip_list, key=lambda trip: trip.total_price)

    @property
    def trip_list_by_date(self):
        return sorted(self.trip_list, key=lambda trip: trip.first_day)

    def get_cheapest_trip(self):
        return self.trip_list_by_price[0]

