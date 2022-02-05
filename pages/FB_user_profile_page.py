

import time
from base.base_driver import BaseDriver
from selenium.webdriver.common.by import  By
from utilities.utils import  Utils

class UserProfile(BaseDriver):
    log = Utils.custom_logger()
    #you can set the logging level with loglevel = logging.DEBUG dont forget to import logging
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains
 
    POST_ELEMENTS = "//div[@role='article']"
    POST_ELEMENTS2 = "//div[@data-pagelet='ProfileTimeline']/*"
    DATE_ELEMENT = "//div[@data-pagelet='ProfileTimeline']/*//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']"

    def getAllDateElements(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.DATE_ELEMENT)
    
