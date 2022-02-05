from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from base.base_driver import BaseDriver
from pages.FB_home_page import FBHomePage
from utilities.utils import Utils

class FBLandingPage(BaseDriver):
    log = Utils.custom_logger()
    
    def __init__(self,driver,achains,email,password):
        super().__init__(driver)
        super().__init__(email)
        super().__init__(password)
        self.driver = driver
        self.achains = achains
        self.email = email
        self.password = password
        
    #locators
    EMAIL_FIELD = "//input[@id='email']"
    PASSWORD_FIELD = "//input[@id='pass']"
    LOGIN_BUTTON = "//button[@name='login']"

    def getEmailField(self):
        return self.driver.find_element(By.XPATH, self.EMAIL_FIELD)    

    def getPasswordField(self):
        return self.driver.find_element(By.XPATH, self.PASSWORD_FIELD) 
    
    def getLoginButton(self):
        return self.driver.find_element(By.XPATH, self.LOGIN_BUTTON)

    def enterEmail(self,email):
        self.log.info("attempting to enter email")
        try:
            self.getEmailField().click()
            self.getEmailField().send_keys(email)
            # self.log.info("Typed {} into email field successfully".format(email))
            self.log.info("Typed email into email field successfully")

        except NoSuchElementException:
            self.log.warning("element did not exist")
            
    def enterPassword(self,password):
        self.log.info("attempting to enter password")
        try:
            self.getPasswordField().click()
            self.getPasswordField().send_keys(password)
            self.log.info("Typed password into password field successfully")
        except NoSuchElementException:
            self.log.warning("element did not exist")

    def clickLogin(self):
        self.log.info("attempting to click login")
        try:
            self.getLoginButton().click()
        except NoSuchElementException:
            self.log.warning("element did not exist")
     
    def loginToFB(self):
        self.enterEmail(self.email)
        self.enterPassword(self.password)
        self.clickLogin()
        # self.log.info("giving 30 seconds to resolve the two factor authentication stuff")
        # time.sleep(30)
        home_page = FBHomePage(self.driver,self.achains)
        return home_page