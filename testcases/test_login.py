#go to yatra
#one way search
#select depart and go to 
# choose a depart date
#click on search flight
#next page is the search flight
#select 1 stop filter
#verify that all the instances show 1 stop
import softest
import pytest
from utilities.utils import Utils
from pages.FB_landing_page import FBLandingPage
from ddt import ddt, data,unpack, file_data


@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()


    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = FBLandingPage(self.driver,self.achains,self.email,self.password)
        self.ut = Utils()
        yield 
        self.lp.driver.get("https://google.com/")

        

    # @file_data("../testdata/data_json.json")
    def test_login_to_fb(self):
        #note four arguments and four per test case in the data tag
        fb_user = self.lp.loginToFB()
        url = fb_user.getUrl()
        self.log.info("THe url of the next page is {}".format(url))
        self.ut.assertOneThing(url,"Facebook.com")

  
    

