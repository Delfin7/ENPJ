from src.locators import LoginPageLocators
from src.pages.base import BasePage
from src.test_base import test_data


class LoginPage(BasePage):
    def login(self, login=test_data.EMAIL, password=test_data.PASSWORD):
        self.fill_input(login, *LoginPageLocators.LOGIN)
        self.fill_input(password, *LoginPageLocators.PASSWORD)
        self.click_button(*LoginPageLocators.SUBMIT)

    def is_incorrect_email(self):
        return self.find_element(*LoginPageLocators.INCORRECT_EMAIL)

    def is_non_existent_account(self):
        return self.find_element(*LoginPageLocators.NON_EXISTENT_ACCOUNT)

    def title(self):
        return self.is_title_matches("Logowanie")