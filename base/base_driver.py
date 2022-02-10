import inspect
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from utilities.utils import  ExceptionHandler
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

    def get_child_element(self,locator_type,parent,child_locator):
        try:
            return parent.find_element(locator_type,child_locator)
        except NoSuchElementException:
            self.log.warning("child element did not exist")
            ExceptionHandler.handle_exception("NoSuchElementException",self.take_screenshot())
            
            return "no child element found"
        except StaleElementReferenceException:
            self.log.warning("stale element exception found in the get child method of the base driver waiting 5 seconds and retrying")
            time.sleep(5)
            try:
                return parent.find_element(locator_type,child_locator)
            except StaleElementReferenceException:
                self.log.warning("Stale reference found in the get child method")
                ExceptionHandler.handle_exception("StaleElementReferenceException",self.take_screenshot())
            
            return "child element reference was stale"

    def scroll_to_element(self,element):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            height = element.size['height']
            script = "window.scrollBy(0,-{});".format(height/2)
            self.driver.execute_script(script)
            return True

        except StaleElementReferenceException:
            ExceptionHandler.handle_exception("StaleElementReferenceException",self.take_screenshot())
            
            self.driver.execute_script("window.scrollBy(0 , 4000 );")
            try:
                time.sleep(2)
                self.log.warning("stale reference but trying again")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                height = element.size['height']
                script = "window.scrollBy(0,-{});".format(height/2)
                self.driver.execute_script(script)
                return True
            except StaleElementReferenceException:
                self.log.warning("stale reference tried twice")
                ExceptionHandler.handle_exception("StaleElementReferenceException",self.take_screenshot())
                
                return False
    
    def take_screenshot(self):
        function_name = inspect.stack()[1][3] + str(int(round(time.time() * 1000))) + ".png"
        screenshot_folder_path = "C:\\Users\\Payan\\Desktop\\FB Project\\screenshots\\"
        destinationFile = screenshot_folder_path + function_name
        self.driver.get_screenshot_as_file(destinationFile)
        return destinationFile


    def zoom_out(self):
        self.driver.execute_script("document.body.style['-webkit-transform'] = \"scale(0.5)\";")