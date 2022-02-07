

from ast import While
from email import utils
import time
from base.base_driver import BaseDriver
from selenium.webdriver.common.by import  By
from utilities.utils import  Utils
from selenium.common.exceptions import NoSuchElementException

class UserProfile(BaseDriver):
    log = Utils.custom_logger()
    #you can set the logging level with loglevel = logging.DEBUG dont forget to import logging
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains
 
    POST_ELEMENTS = "//div[@data-pagelet='ProfileTimeline']//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']"
    DATE_ELEMENT_CHILD = ".//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']"
    MOVE_TO_TRASH_BUTTON = "//span[normalize-space()='Move to trash']"
    FINALIZE_MOVE_TO_TRASH_BUTTON = "//div[@aria-label='Move'][1]"
    CANCEL_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Cancel'])[2]"
    POSTER_NAME_CHILD = ".//strong"
    USERS_NAME = "//body//div//h1[1]"
    OPTIONS_FOR_THIS_POST = ".//div[@aria-label='Actions for this post'][1]"

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

    def get_options_for_this_post(self,post):
        return self.get_child_elemenet(By.XPATH,post,self.OPTIONS_FOR_THIS_POST)
    
    def click_options_for_this_post(self,post):
        options = self.get_options_for_this_post(post)
        self.log.info("attempting to click the options for this post button")
        if type(options) == str:
            return options
        else:
            options.click()
            self.log.info("clicked on options button successfully")

    def get_move_to_trash_button(self):
        return self.driver.find_element(By.XPATH,self.MOVE_TO_TRASH_BUTTON)
        
    def click_move_to_trash_button(self):
        self.log.info("attempting to click move to trash button")
        try:
            self.get_move_to_trash_button().click()
            self.log.info("clicked move to trash button successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")

    def get_finalize_move_to_trash_button(self):
        return self.driver.find_element(By.XPATH,self.FINALIZE_MOVE_TO_TRASH_BUTTON)

    def get_cancel_move_to_trash_button(self):
        return self.driver.find_element(By.XPATH,self.CANCEL_MOVE_TO_TRASH_BUTTON)
    
    def click_finalize_move_to_trash_button(self):
        self.log.info("attempting to click on the final move to trash button")
        try:
            self.get_finalize_move_to_trash_button().click()
            self.log.info("clicked on the final move to trash button successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")

    def click_cancel_move_to_trash_button(self):
        self.log.info("attempting to click on the cancel move to trash button")
        try:
            self.get_cancel_move_to_trash_button().click()
            self.log.info("clicked on the cancel move to trash button successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")
    
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
                    self.log.info("we found the first post that is before the given date of {dateGiven} \n the number of loops it took to get here was {numberOfLoops} \n the index of the first post is {indexOfPost} \n".format(dateGiven = dateOfInterestTempVar, numberOfLoops = numberOfLoops,indexOfPost = indexOfPost))    
                    self.fake_delete_post(lastPost)
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

    def delete_post(self,post):
        height = post.size['height']
        self.scroll_to_element(post)
        script = "window.scrollBy(0,-{});".format(height/2)
        self.driver.execute_script(script)
        self.click_options_for_this_post(post)
        time.sleep(4)
        self.click_move_to_trash_button()
        time.sleep(4)
        self.click_finalize_move_to_trash_button()

    def fake_delete_post(self,post):
        height = post.size['height']
        self.scroll_to_element(post)
        script = "window.scrollBy(0,-{});".format(height/2)
        self.driver.execute_script(script)
        self.click_options_for_this_post(post)
        time.sleep(4)
        self.click_move_to_trash_button()
        time.sleep(4)
        self.click_cancel_move_to_trash_button()



        



            
            


    
