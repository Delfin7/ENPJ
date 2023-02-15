from src.locators import OptionsPageLocators
from src.pages.base import BasePage


class OptionsPage(BasePage):
    def change_password(self):
        self.click_button(*OptionsPageLocators.CHANGE_PASSWORD)

    def set_language_polish(self):
        self.select("Polski", *OptionsPageLocators.LANGUAGE)

    def set_language_english(self):
        self.select("Angielski", *OptionsPageLocators.LANGUAGE)

    def set_language_german(self):
        self.select("Niemiecki", *OptionsPageLocators.LANGUAGE)

    def check_sign_language(self):
        if not self.is_selected(*OptionsPageLocators.SIGN_LANGUAGE):
            self.click_button(*OptionsPageLocators.SIGN_LANGUAGE)

    def uncheck_sign_language(self):
        if self.is_selected(*OptionsPageLocators.SIGN_LANGUAGE):
            self.click_button(*OptionsPageLocators.SIGN_LANGUAGE)

    def title(self):
        return self.is_title_matches("Opcje")

    def save(self):
        self.click_button(*OptionsPageLocators.SAVE)

    def is_saved(self):
        return self.get_text(*OptionsPageLocators.OPTIONS_SAVED) == "Ustawienia zostały zaktualizowane!"