import calendar


class SkyscannerScrapData:

    def __init__(self,ori, dest, adults, year, month):
        self.ori = ori
        self.dest = dest
        self.adults = adults
        self.year = year
        self.month = month

        year_aux = "%02d" % year
        month_aux = "%02d" % month
        self.date = year_aux + month_aux


class RyanairScrapData:

    def __init__(self,ori, dest, adults, year, month):
        self.ori = ori
        self.dest = dest
        self.adults = adults
        self.year = year
        self.month = month
        day = calendar.monthrange(2018, self.month)[1]
        self.date = "{}-{}-{}".format(year, month, day)