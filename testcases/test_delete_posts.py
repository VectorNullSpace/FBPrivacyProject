
import softest
import pytest
from utilities.utils import Utils
from pages.FB_landing_page import FBLandingPage
from ddt import ddt, data,unpack, file_data
import time


@pytest.mark.usefixtures("setup")
@ddt
class TestDeleteOldPosts(softest.TestCase):
    log = Utils.custom_logger()


    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = FBLandingPage(self.driver,self.achains,self.email,self.password)
        self.ut = Utils()
        yield 
        self.lp.driver.get("https://google.com/")

        

    @file_data("../testdata/data_json.json")
    def test_delete_fb_posts(self,dateOfInterest):
        #note four arguments and four per test case in the data tag
        fb_home = self.lp.loginToFB()
        time.sleep(2)
        fb_userProfile = fb_home.navigateToUserProfile()
        usersName = fb_userProfile.get_users_name()
        indexOfFirstPost = fb_userProfile.find_first_post_before_date(dateOfInterest)
        fb_userProfile.go_through_posts_and_delete(dateOfInterest,usersName,indexOfFirstPost)

        assert 2+2 == 4
        

  
    

