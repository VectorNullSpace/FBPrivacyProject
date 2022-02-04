

import time
from base.base_driver import BaseDriver
from selenium.webdriver.common.by import  By
from utilities.utils import  Utils

class SearchFlightResults(BaseDriver):
    log = Utils.custom_logger()
    #you can set the logging level with loglevel = logging.DEBUG dont forget to import logging
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
 
    #locators
    FILTER_BY_1_STOP_BUTTON = "//div[contains(@class,'filter-stops')]//label[2]"
    FILTER_BY_2_STOP_BUTTON = "//div[contains(@class,'filter-stops')]//label[3]"
    FILTER_BY_NON_STOP_BUTTON = "//div[contains(@class,'filter-stops')]//label[1]"
    SEARCH_FLIGHT_RESULTS = "//span[contains(text(),'Non Stop') or contains(text(), '1 Stop') or contains(text(), '2 Stop')]"

    def get_filter_by_one_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_1_STOP_BUTTON)
    
    def get_filter_by_two_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_2_STOP_BUTTON)

    def get_filter_by_non_stop_button(self):
        return self.driver.find_element(By.XPATH, self.FILTER_BY_NON_STOP_BUTTON)

    def get_search_flight_results(self):
        return self.wait_for_presence_of_all_elements(By.XPATH, self.SEARCH_FLIGHT_RESULTS)

    def filter_flights_by_stop(self, by_stop):
        if by_stop == "1 Stop":
            self.get_filter_by_one_stop_button().click()
            self.log.info("Selected flights with 1 stop")
            time.sleep(4)
        elif by_stop == "2 Stops":
            self.get_filter_by_two_stop_button().click()
            self.log.info("Selected flights with 2 stops")
            time.sleep(4)
        elif by_stop == "Non Stop":
            self.get_filter_by_non_stop_button().click()
            self.log.info("Selected non stop flights")
            time.sleep(4)
        else:
            self.log.info("Please provide valid filter option")
        