from src.locators import SignupPageLocators
from src.pages.base import BasePage


class SignupPage(BasePage):
    def signup(self, login, username, password, password_confirm):
        self.fill_input(login, *SignupPageLocators.EMAIL)
        self.fill_input(username, *SignupPageLocators.USERNAME)
        self.fill_input(password, *SignupPageLocators.PASSWORD)
        self.fill_input(password_confirm, *SignupPageLocators.PASSWORD_CONFIRM)
        self.click_button(*SignupPageLocators.SUBMIT)

    def is_incorrect_email(self):
        return self.find_element(*SignupPageLocators.INCORRECT_EMAIL)

    def is_incorrect_password(self):
        return self.find_element(*SignupPageLocators.INCORRECT_PASSWORD)

    def is_not_same_password(self):
        return self.find_element(*SignupPageLocators.NOT_SAME_PASSWORD)

    def is_existing_email(self):
        return self.find_element(*SignupPageLocators.EXISTING_EMAIL)

    def is_existing_username(self):
        return self.find_element(*SignupPageLocators.EXISTING_USERNAME)

    def title(self):
        return self.is_title_matches("Rejestracja")