

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
 
    POST_ELEMENTS = "//div[@data-pagelet='ProfileTimeline']//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']"
    DATE_ELEMENT_CHILD = ".//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']"
    MOVE_TO_TRASH_BUTTON = "(//div[@role='menuitem'])[9]"
    FINALIZE_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Move'])[1]"
    CANCEL_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Cancel'])[2]"
    POSTER_NAME_CHILD = ".//strong"
    USERS_NAME = "//body//div//h1[1]"

    def get_users_name(self):
        # return self.driver.find_element(By.XPATH,self.USERS_NAME).get_attribute("textContent")
        return "JP Payano"

    def get_all_posts(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.POST_ELEMENTS)

    def get_date_from_post(self,post):
        child =  self.get_child_elemenet(By.XPATH,post,self.DATE_ELEMENT_CHILD)
        if type(child) == str:
            return child
        else:
            return child.get_attribute("aria-label")

    def get_name_of_poster(self,post):
        child =  self.get_child_elemenet(By.XPATH,post,self.POSTER_NAME_CHILD)
        if type(child) == str:
            return child
        else:
            return child.text


    def go_through_posts(self):
        username = self.get_users_name()
        self.log.info(username)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        # self.zoom_out()
        posts = self.get_all_posts()
        totalPosts = len(posts)
        match = False
        while match == False:
            self.log.info("THE LENGTH OF THE LIST IS {}".format(len(posts)))
            for post in posts:
                self.scroll_to_element(post)
                date = self.get_date_from_post(post)
                self.log.info(date)
                self.log.info("Does the date match the proper format? {}".format(Utils.validate(date)))
                poster = self.get_name_of_poster(post)
                self.log.info(poster)
                self.log.info("text match returns {}".format(Utils.does_text_match(username,poster)))
            
            posts = self.get_all_posts()
            if len(posts) == totalPosts:
                match = True
            else:
                totalPosts = len(posts)
            
            


    
