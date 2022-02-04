import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import  EdgeChromiumDriverManager
from selenium.webdriver.common.action_chains import  ActionChains

from utilities.utils import Utils



@pytest.fixture(scope="class")
def setup(request,browser,email,password):
    log = Utils.custom_logger()
    global driver 

    #launch browser and opening the travel website
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        s=Service(ChromeDriverManager().install())
        driver= webdriver.Chrome(service=s, options=options) 

    elif browser == "edge":
        s=Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=s) 

    elif browser == "firefox":
        s=Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=s) 

    else:
        log.warning("please provide a proper browser")
    


    driver.implicitly_wait(10)
    driver.get("https://www.facebook.com/")
    achains = ActionChains(driver)
    driver.maximize_window()
    request.cls.driver = driver
    request.cls.achains = achains
    request.cls.email = email
    request.cls.password = password
    yield
    driver.close()

def pytest_addoption(parser):
    parser.addoption("--browser", default = "chrome")
    parser.addoption("--email")
    parser.addoption("--password")

@pytest.fixture(scope="class",autouse=True)
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="class",autouse=True)
def email(request):
    return request.config.getoption("--email")

@pytest.fixture(scope="class",autouse=True)
def password(request):
    return request.config.getoption("--password")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        # always add url to report
        extra.append(pytest_html.extras.url("http://www.facebook.com/"))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            #file_name = str(int(round(time.time() * 1000))) + ".png"
            file_name = report.nodeid.replace("::","_") + ".png"
            destinationFile = os.path.join(report_directory,file_name)
            driver.save_screenshot(destinationFile)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:300px;height:200px"'\
                    'onclick="window.open(this.src)" align="right"/></div>'%file_name

            extra.append(pytest_html.extras.html(html))
        report.extra = extra

def pytest_html_report_title(report):
    report.title = "JP's Automation Report"