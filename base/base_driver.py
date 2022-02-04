
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
#for anything extending the driver


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def page_scroll(self, go_to_top = True):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        match = False
        while (match == False):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                match = True
            last_height = new_height

        if go_to_top == True:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
        
        time.sleep(4)

        

    def wait_for_presence_of_all_elements(self, locator_type,locator):
        wait = WebDriverWait(self.driver,10)
        list_of_elements = wait.until(EC.presence_of_all_elements_located((locator_type,locator)))
        # allstops = self.driver.find_elements(By.XPATH,"//span[contains(text(),'Non Stop') or contains(text(), '1 Stop') or contains(text(), '2 Stop')]")
        return list_of_elements