from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.pages.base import BasePage
from src.test_base import test_data


class BaseTest(TestCase, BasePage):
    def setUp(self):
        if test_data.BROWSER == "Chrome":
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        elif test_data.BROWSER == "Firefox":
            self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        elif test_data.BROWSER == "Edge":
            self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        elif test_data.BROWSER == "Edge":
            self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
        self.go_to_main_site()

    def tearDown(self):
        self.driver.quit()