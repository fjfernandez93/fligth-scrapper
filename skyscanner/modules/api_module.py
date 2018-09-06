from modules.ryanair_scrapper import RyanairScrapper
from modules.skyscanner_scrapper import SkyscannerScrapper
import threading
from model.scrapping_model import RyanairScrapData, SkyscannerScrapData


def scrap_site(site, ori, dest, year, month):

    if site == 'ryanair':
        obj = RyanairScrapData(ori, dest, 2, year, month)
        scrp = RyanairScrapper()
        process = threading.Thread(target=scrp.scrap_ryanair, args=(obj,))
    elif site == 'skyscanner':
        obj = SkyscannerScrapData(ori, dest, 2, year, month)
        scrp = SkyscannerScrapper()
        process = threading.Thread(target=scrp.scrap_skyscanner, args=(obj,))

    process.start()
