from src.locators import NavigationBarLocators
from src.pages.base import BasePage


class NavigationBar(BasePage):
    def go_to_login(self):
        self.click_button(*NavigationBarLocators.LOGIN)

    def go_to_signup(self):
        self.click_button(*NavigationBarLocators.SIGNUP)

    def go_to_prepare_learning(self):
        self.click_button(*NavigationBarLocators.PREPARE_LEARNING)

    def go_to_prepare_exam(self):
        self.click_button(*NavigationBarLocators.PREPARE_EXAM)

    def go_to_statistics(self):
        self.click_button(*NavigationBarLocators.STATISTICS)

    def go_to_options(self):
        self.click_button(*NavigationBarLocators.OPTIONS)

    def logout(self):
        self.click_button(*NavigationBarLocators.LOGOUT)