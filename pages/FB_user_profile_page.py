

from ast import While
from email import utils
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
        dateOfInterestTempVar = "December 9, 2020"
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
                if Utils.validate(date):
                    if Utils.is_before(dateOfInterestTempVar,date):
                        self.log.info("the current post is before the date of interest ({})".format(dateOfInterestTempVar))
                    else:
                        self.log.info("the current post is NOT before the date of interest ({})".format(dateOfInterestTempVar))
                

            
            posts = self.get_all_posts()
            if len(posts) == totalPosts:
                match = True
            else:
                totalPosts = len(posts)

    def find_first_post_before_date(self):
        dateOfInterestTempVar = "December 9, 2018"
        self.log.info("searching for first post that is before the given date ({})".format(dateOfInterestTempVar))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        posts = self.get_all_posts()
        totalPosts = len(posts)
        match = False
        numberOfLoops = 0
        while match == False:
            lastPost = posts[-1]
            self.scroll_to_element(lastPost)
            time.sleep(1)
            date = self.get_date_from_post(lastPost)
            self.log.info(date)
            self.log.info("Does the date match the proper format? {}".format(Utils.validate(date)))
            if Utils.validate(date):
                if Utils.is_before(dateOfInterestTempVar,date):
                    self.log.info("the current post is before the date of interest ({})".format(dateOfInterestTempVar))
                    self.log.info("We found the first post!")
                    totalPosts = len(posts)
                    poster = self.get_name_of_poster(lastPost)
                    self.log.info(poster)
                    self.log.info(date)
                    indexOfPost = totalPosts - 1
                    self.log.info("we found the first post that is before the given date of {dateGiven} \n the number of loops it took to get here was {numberOfLoops} \n the index of the first post is {indexOfPost} \n".format(dateGiven = dateOfInterestTempVar, numberOfLoops = numberOfLoops,indexOfPost = indexOfPost -1))    
                    match = True
                else:
                    self.log.info("the current post is NOT before the date of interest ({})".format(dateOfInterestTempVar))
            
            numberOfLoops = numberOfLoops + 1
            posts = self.get_all_posts()
            if len(posts) == totalPosts:
                self.log.info("there were no posts that matched the criteria requested for deletion")
                indexOfPost = -1 
                match = True
            else:
                totalPosts = len(posts)

        return indexOfPost


        



            
            


    
