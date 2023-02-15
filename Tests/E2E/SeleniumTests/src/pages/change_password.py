from src.locators import ChangePasswordPageLocators
from src.pages.base import BasePage


class ChangePasswordPage(BasePage):
    def change_password(self, current_password, new_password, new_password_confirm):
        self.fill_input(current_password, *ChangePasswordPageLocators.CURRENT_PASSWORD)
        self.fill_input(new_password, *ChangePasswordPageLocators.NEW_PASSWORD)
        self.fill_input(new_password_confirm, *ChangePasswordPageLocators.NEW_PASSWORD_CONFIRM)
        self.click_button(*ChangePasswordPageLocators.SUBMIT)

    def is_password_changed(self):
        return self.find_element(*ChangePasswordPageLocators.PASSWORD_CHANGED)

    def is_incorrect_current_password(self):
        return self.find_element(*ChangePasswordPageLocators.INCORRECT_CURRENT_PASSWORD)

    def is_incorrect_new_password(self):
        return self.find_element(*ChangePasswordPageLocators.INCORRECT_NEW_PASSWORD) and \
               self.find_element(*ChangePasswordPageLocators.INCORRECT_NEW_PASSWORD2)

    def title(self):
        return self.is_title_matches("Zmień hasło")