
"""
This class is temporal until I implement some kind of solution with semaphores or anything better to
only allow a certain number of concurrent scrappers
"""

class GlobalState():

    MAX_CURRENT_SCRAPPERS = 3
    current_scrappers = 0

    @staticmethod
    def can_start_scrapper():
        if GlobalState.current_scrappers < GlobalState.MAX_CURRENT_SCRAPPERS:
            GlobalState.current_scrappers = GlobalState.current_scrappers + 1
            return True
        else:
            return False

    @staticmethod
    def finished_scrapper():
        GlobalState.current_scrappers = GlobalState.current_scrappers - 1