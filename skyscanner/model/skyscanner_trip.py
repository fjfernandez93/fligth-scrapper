import datetime
import model.skyscanner_dao


class SkyscannerTrip:

    def __init__(self, ori_combi, dest_combi, ori_date, dest_date):
        self.ori_combi = ori_combi
        self.dest_combi = dest_combi
        self.ori_date = ori_date
        self.dest_date = dest_date
        self.ori_price = -2
        self.dest_price = -2
        self.ori_site = ""
        self.dest_site = ""

    @property
    def total_price(self):
        return round(self.ori_price + self.dest_price, 2)

    def set_price(self):
        dao = model.skyscanner_dao.SkyscannerDAO()

        tuple_ori = dao.get_price_for_ticket(self.ori_date.day, self.ori_date.month, self.ori_date.year,
                                                  self.ori_combi[0], self.ori_combi[1])
        self.ori_price = tuple_ori[0]
        self.ori_site = tuple_ori[1]

        tuple_dest = dao.get_price_for_ticket(self.dest_date.day, self.dest_date.month, self.dest_date.year,
                                                   self.dest_combi[0], self.dest_combi[1])
        self.dest_price = tuple_dest[0]
        self.dest_site = tuple_dest[1]
