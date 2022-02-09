
import traceback
from ast import While
from email import utils
import time
from base.base_driver import BaseDriver
from selenium.webdriver.common.by import  By
from utilities.utils import  Utils, ExceptionHandler
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

class UserProfile(BaseDriver):
    log = Utils.custom_logger()
    #you can set the logging level with loglevel = logging.DEBUG dont forget to import logging
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains
 
    POST_ELEMENTS = "//div[@data-pagelet='ProfileTimeline']//div[@class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0']"
    DATE_ELEMENT_CHILD = ".//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']"
    #".//div[@class='qzhwtbm6 knvmm38d'][2]//a[@href='#']" this is the original testing if removing the href part causes issues
    MOVE_TO_TRASH_BUTTON = "//span[normalize-space()='Move to trash']"
    FINALIZE_MOVE_TO_TRASH_BUTTON = "//div[@aria-label='Move'][1]"
    CANCEL_MOVE_TO_TRASH_BUTTON = "(//div[@aria-label='Cancel'])[2]"
    POSTER_NAME_CHILD = ".//strong"
    POSTER_NAME_CHILD_FULL = ".//strong//.."
    USERS_NAME = "//body//div//h1[1]//.."
    OPTIONS_FOR_THIS_POST = ".//div[@aria-label='Actions for this post'][1]"

    def get_users_name(self):
        # return self.driver.find_element(By.XPATH,self.USERS_NAME).text
        return "JP Payano"
        

    def get_all_posts(self):
        return self.wait_for_presence_of_all_elements(By.XPATH,self.POST_ELEMENTS)

    def get_date_from_post(self,post):
        child =  self.get_child_element(By.XPATH,post,self.DATE_ELEMENT_CHILD)
        if type(child) == str:
            return child
        else:
            return child.get_attribute("aria-label")

    def get_name_of_poster(self,post):
        child =  self.get_child_element(By.XPATH,post,self.POSTER_NAME_CHILD)
        if type(child) == str:
            return child
        else:
            return child.text

    def get_name_of_posterFULL(self,post):
        child =  self.get_child_element(By.XPATH,post,self.POSTER_NAME_CHILD_FULL)
        if type(child) == str:
            return child
        else:
            return child.text
    
    def get_options_for_this_post(self,post):
        return self.get_child_element(By.XPATH,post,self.OPTIONS_FOR_THIS_POST)
    
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
            ExceptionHandler.handle_exception("NoSuchElementException",self.take_screenshot())
            self.log.warning(traceback.extract_stack())

        except ElementClickInterceptedException:
            ExceptionHandler.handle_exception("ElementClickInterceptedException",self.take_screenshot())
            self.log.warning(traceback.extract_stack())

            self.log.warning("element click intercepted attempting to move a little and retry")
            script = "window.scrollBy(0,400);"
            self.driver.execute_script(script)
            self.get_move_to_trash_button().click()

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
            ExceptionHandler.handle_exception("NoSuchElementException",self.take_screenshot())
            self.log.warning(traceback.extract_stack())
            


    def click_cancel_move_to_trash_button(self):
        self.log.info("attempting to click on the cancel move to trash button")
        try:
            self.get_cancel_move_to_trash_button().click()
            self.log.info("clicked on the cancel move to trash button successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")
            ExceptionHandler.handle_exception("NoSuchElementException",self.take_screenshot())
            self.log.warning(traceback.extract_stack())

    
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

    def find_first_post_before_date(self,dateOfInterest):
        self.log.info("searching for first post that is before the given date ({})".format(dateOfInterest))
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
            self.log.debug(date)
            self.log.debug("Does the date match the proper format? {}".format(Utils.validate(date)))
            if Utils.validate(date):
                if Utils.is_before(dateOfInterest,date):
                    self.log.info("the current post is before the date of interest ({})".format(date))
                    self.log.info("We found the first post!")
                    totalPosts = len(posts)
                    poster = self.get_name_of_poster(lastPost)
                    self.log.info(poster)
                    self.log.info(date)
                    indexOfPost = totalPosts - 1
                    self.log.info("we found the first post that is before the given date of {dateGiven} \n the number of loops it took to get here was {numberOfLoops} \n the index of the first post is {indexOfPost} \n".format(dateGiven = dateOfInterest, numberOfLoops = numberOfLoops,indexOfPost = indexOfPost))    
                    indexOfPost = self.go_through_posts_backwards(dateOfInterest)
                    match = True
                    break
                else:
                    self.log.debug("the current post is NOT before the date of interest ({})".format(date))
            
            numberOfLoops = numberOfLoops + 1
            posts = self.get_all_posts()
            if len(posts) == totalPosts:
                #give it a second to load and check again. occasionally there is a sync issue
                time.sleep(4)
                self.log.info("waiting in case of sync issue")
                posts = self.get_all_posts()
                if len(posts) == totalPosts:
                    self.log.info("there were no posts that matched the criteria requested for deletion")
                    indexOfPost = -1 
                    match = True
                else:
                    totalPosts = len(posts)
            else:
                totalPosts = len(posts)

        return indexOfPost

    def delete_post(self,post):
        try:
            self.scroll_to_element(post)
            self.click_options_for_this_post(post)
            self.click_move_to_trash_button()
            self.click_finalize_move_to_trash_button()
            self.log.info("post has been deleted")
            return True
        except:
            self.log.warning("post failed to delete")
            return False

    def fake_delete_post(self,post):
        try:
            self.scroll_to_element(post)
            self.click_options_for_this_post(post)
            self.click_move_to_trash_button()
            time.sleep(2)
            self.click_cancel_move_to_trash_button()
            self.log.info("post has been fake deleted")
            return True
        except:
            self.log.warning("post failed to fake delete")
            return False

    def go_through_posts_backwards(self,dateOfInterest):
        posts = self.get_all_posts()
        totalPosts = len(posts)
        match = False
        numberOfPostsGoneThrough = 0
        while match == False:
            for post in reversed(posts):
                numberOfPostsGoneThrough = numberOfPostsGoneThrough + 1
                self.scroll_to_element(post)
                time.sleep(1)
                date = self.get_date_from_post(post)
                self.log.debug(date)
                self.log.debug("Does the date match the proper format? {}".format(Utils.validate(date)))
                if Utils.validate(date):
                    if not Utils.is_before(dateOfInterest,date):
                        self.log.info("this is the latest post before the date of interest ({})".format(date))
                        self.log.info("We found the first post(to ignore)!")
                        totalPosts = len(posts)
                        poster = self.get_name_of_poster(post)
                        self.log.info(poster)
                        self.log.info(date)
                        indexOfPost = totalPosts - numberOfPostsGoneThrough
                        self.log.info("we found the first post that is before the given date of {dateGiven} \n  the index of the first post is {indexOfPost} \n".format(dateGiven = dateOfInterest,indexOfPost = indexOfPost))
                        match = True
                        break
                    else:
                        self.log.debug("the current post is NOT before the date of interest ({})".format(date))

        return indexOfPost

    def postMeetsCriteria(self,post,dateOfInterest,usersName):
        date = self.get_date_from_post(post)
        poster = self.get_name_of_poster(post)
        fullTextOfPoster = self.get_name_of_posterFULL(post)
        meetsCriteria = False
        self.log.info("the criteria is as follows username: {} date:{}".format(usersName,dateOfInterest))
        self.log.info("date of post: {} name of poster: {} fullText of name: {}".format(date,poster,fullTextOfPoster))
        if Utils.validate(date):
            meetsCriteria = (Utils.is_before(dateOfInterest,date) and Utils.check_poster_text(usersName,fullTextOfPoster))
        
        if meetsCriteria ==True:
            self.log.info("current post meets the criteria")
        else:
            self.log.info("the current post does NOT meet criteria")
            
        return meetsCriteria
        
    def go_through_posts_and_delete(self,dateOfInterest,usersName,startingPostIndex):
        if startingPostIndex == -1:
            self.log.warning("there are no posts to delete as the search function found no post before the given date")
        else:
            posts = self.get_all_posts()
            totalPosts = len(posts)
            match = False
            numberOfPostsLookedAt = 0
            numberOfPostsDeleted = 0
            numberOfLoops = 0
            totalPostslookedat = 0
            totalPostsDeleted = 0
            while match == False:
                for i in range(startingPostIndex,totalPosts):
                    totalPostslookedat = totalPostslookedat + 1
                    numberOfPostsLookedAt = numberOfPostsLookedAt + 1
                    post = posts[i]
                    self.log.info("this is post number {}".format(numberOfPostsLookedAt))
                    self.scroll_to_element(post)
                    time.sleep(2)
                    if self.postMeetsCriteria(post,dateOfInterest,usersName):
                        if self.delete_post(post):
                            numberOfPostsDeleted = numberOfPostsDeleted + 1
                            totalPostsDeleted = totalPostsDeleted + 1

                        

                if totalPostslookedat > 30:
                    self.log.info("the number of posts looked at are {numberOfPosts} and the number of deleted among them are {numberOfPostsDeleted}".format(numberOfPosts = totalPostslookedat,numberOfPostsDeleted=totalPostsDeleted))
                    self.log.info("the number of loops around were {}".format(numberOfLoops))
                    match = True
                    break
                else:
                    self.log.info("the number of total posts in the DOM is {}".format(totalPosts))
                    self.log.info("The number of posts gone through last loop are {}".format(numberOfPostsLookedAt))
                    self.log.info("The number of posts deleted last time were {}".format(numberOfPostsDeleted))
                    numberOfPostsLookedAt = 0
                    numberOfPostsDeleted = 0
                    posts = self.get_all_posts()
                    startingPostIndex = startingPostIndex + totalPostslookedat - totalPostsDeleted 
                    totalPosts = len(posts)
                    numberOfLoops = numberOfLoops + 1

 


            
            


    
