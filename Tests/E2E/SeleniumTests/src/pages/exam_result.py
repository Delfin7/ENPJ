from src.locators import ExamResultPageLocators
from src.pages.base import BasePage


class ExamResultPage(BasePage):
    def check_information(self, category, points):
        if points < 68:
            result = "NEGATYWNY"
        else:
            result = "POZYTYWNY"
        finished_exam = self.find_element(*ExamResultPageLocators.FINISHED_EXAM)
        category_is_correct = self.get_text(*ExamResultPageLocators.CATEGORY) == "Kategoria " + category
        result_is_correct = self.get_text(*ExamResultPageLocators.RESULT) == f"Uzyskałeś wynik {result}, zdobywając {points} na 74 punkty (wymagane: 68)."

        return finished_exam and category_is_correct and result_is_correct

    def title(self):
        return self.is_title_matches("Wynik z egzaminu")

    def check_answers(self):
        self.click_button(*ExamResultPageLocators.CHECK_ANSWERS)