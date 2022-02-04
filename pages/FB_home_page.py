from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from base.base_driver import BaseDriver
from utilities.utils import Utils


class FBHomePage(BaseDriver):
    log = Utils.custom_logger()
    
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains

