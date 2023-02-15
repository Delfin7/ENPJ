from src.locators import PrepareLearningPageLocators
from src.pages.base import BasePage


class PrepareLearningPage(BasePage):
    def prepare_learning_b_module_1(self):
        self.click_button(*PrepareLearningPageLocators.CATEGORY_B)
        self.click_button(*PrepareLearningPageLocators.MODULE_FIRST)

    def reset_progress(self, category, module):
        self.delete_cookie(f"category{category}m{module}")

    def title(self):
        return self.is_title_matches("Przygotowanie nauki")
