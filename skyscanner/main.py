

import modules.skyscanner_scrapper
import modules.ryanair_scrapper
from api_rest.skyscanner_api import start_api
from model import skyscanner_dao


from model.scrapping_model import SkyscannerScrapData, RyanairScrapData

#skyscanner_scrap_data = SkyscannerScrapData('mad', 'waw', 2, 18, 10)
#modules.skyscanner_scrapper.scrap_skyscanner(skyscanner_scrap_data)

#ryan = RyanairScrapData('mad', 'wmi', 2, 2018, 10)
#modules.ryanair_scrapper.scrap_ryanair(ryan)

start_api()

#dao = skyscanner_dao.SkyscannerDAO()

#a = dao.get_price_for_ticket(10,12,2018,"mad", "wmi")

#print(a)