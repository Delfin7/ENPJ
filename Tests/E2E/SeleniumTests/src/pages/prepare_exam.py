from src.locators import PrepareExamPageLocators
from src.pages.base import BasePage


class PrepareExamPage(BasePage):
    def prepare_exam_b(self):
        self.click_button(*PrepareExamPageLocators.CATEGORY_B)

    def started_exam_exists(self):
        continue_check_exam = self.get_text(*PrepareExamPageLocators.CONTINUE_CHECK_EXAM)
        return continue_check_exam == "Kontynuuj rozpoczęty egzamin"

    def continue_exam_check_answers(self):
        self.click_button(*PrepareExamPageLocators.CONTINUE_CHECK_EXAM)

    def title(self):
        return self.is_title_matches("Przygotowanie egzaminu")