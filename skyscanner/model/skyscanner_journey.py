import datetime


class SkyscannerJourney:

    def __init__(self, ori, dest, day, month, year):
        self.ori = ori
        self.dest = dest
        self.date = datetime.date(year+2000, month, day)