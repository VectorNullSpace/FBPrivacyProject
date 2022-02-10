from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from base.base_driver import BaseDriver
from utilities.utils import Utils , ExceptionHandler
from pages.FB_user_profile_page import UserProfile
import traceback


class FBHomePage(BaseDriver):
    log = Utils.custom_logger()
    
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains

    USER_PROFILE = "//div[@role='navigation']//a[@href='/me/']"

    def getUserProfile(self):
        return self.driver.find_element(By.XPATH, self.USER_PROFILE)

    def clickUserProfile(self):
        self.log.info("attempting to click user profile")
        try:
            # self.achains.move_to_element(self.getUserProfile()).click().perform()
            self.getUserProfile().click()
            self.log.info("clicked user profile successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")
            ExceptionHandler.handle_exception("NoSuchElementException",self.take_screenshot())
            


    def navigateToUserProfile(self):
        self.clickUserProfile()
        user_profile = UserProfile(self.driver,self.achains)
        time.sleep(10)
        return user_profile