from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import urllib.parse
from src.test_base import test_data


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def find_element(self, *locators):
        return self.driver.find_element(*locators)

    def fill_input(self, value, *locators):
        self.wait.until(EC.visibility_of_element_located(locators))
        self.find_element(*locators).send_keys(value)

    def click_button(self, *locators):
        self.wait.until(EC.element_to_be_clickable(locators))
        self.find_element(*locators).click()

    def select(self, text, *locators):
        self.wait.until(EC.visibility_of_element_located(locators))
        Select(self.find_element(*locators)).select_by_visible_text(text)

    def is_title_matches(self, title):
        self.wait.until(EC.title_is(title))
        return title in self.driver.title

    def alert_accept(self):
        self.wait.until(EC.alert_is_present())
        Alert(self.driver).accept()

    def alert_cancel(self):
        self.wait.until(EC.alert_is_present())
        Alert(self.driver).dismiss()

    def get_text(self, *locators):
        return self.find_element(*locators).text

    def get_attributes(self, *locators, src=False):
        element = self.find_element(*locators)
        attributes = {"displayed": element.is_displayed(),
                      "background-color": element.value_of_css_property('background-color')}
        if src:
            attributes["src"] = urllib.parse.unquote(element.get_attribute("src"))
        return attributes

    def go_to_main_site(self):
        self.driver.get(test_data.APP_URL)

    def is_selected(self, *locators):
        self.wait.until(EC.visibility_of_element_located(locators))
        return self.find_element(*locators).is_selected()

    def delete_cookie(self, name):
        self.driver.delete_cookie(name)