

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
    DATE_ELEMENT_CHILD = ".//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']"
    MOVE_TO_TRASH_BUTTON = "(//div[@role='menuitem'])[9]"
    FINALIZE_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Move'])[1]"
    CANCEL_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Cancel'])[2]"
    POSTER_NAME_CHILD = ".//strong"
    USERS_NAME = "//h1"

    def get_users_name(self):
        return self.driver.find_element(By.XPATH,self.USERS_NAME).text

    def getAllPosts(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.POST_ELEMENTS2)

    def getDateFromPost(self,post):
        child =  self.get_child_elemenet(By.XPATH,post,self.DATE_ELEMENT_CHILD)
        if type(child) == str:
            return child
        else:
            return child.get_attribute("aria-label")

    def getNameOfPoster(self,post):
        child =  self.get_child_elemenet(By.XPATH,post,self.POSTER_NAME_CHILD)
        if type(child) == str:
            return child
        else:
            return child.text

    
