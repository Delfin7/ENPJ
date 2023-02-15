from src.locators import ExamCheckAnswersPageLocators
from src.pages.base import BasePage
from selenium.webdriver.support.color import Color


class ExamCheckAnswersPage(BasePage):
    def get_points(self):
        return self.get_text(*ExamCheckAnswersPageLocators.POINTS)

    def get_category(self):
        return self.get_text(*ExamCheckAnswersPageLocators.CATEGORY)

    def get_image_attributes(self):
        return self.get_attributes(*ExamCheckAnswersPageLocators.IMAGE, src=True)

    def get_video_attributes(self):
        return self.get_attributes(*ExamCheckAnswersPageLocators.VIDEO, src=True)

    def get_question(self):
        return self.get_text(*ExamCheckAnswersPageLocators.QUESTION)

    def check_answers(self, correct_answer, selected_answer):
        answer_1_color = Color.from_string(
            self.get_attributes(*ExamCheckAnswersPageLocators.ANSWER_1)['background-color']).hex
        answer_2_color = Color.from_string(
            self.get_attributes(*ExamCheckAnswersPageLocators.ANSWER_2)['background-color']).hex
        answer_3_color = Color.from_string(
            self.get_attributes(*ExamCheckAnswersPageLocators.ANSWER_3)['background-color']).hex
        answer_1_text = self.get_text(*ExamCheckAnswersPageLocators.ANSWER_1)
        answer_2_text = self.get_text(*ExamCheckAnswersPageLocators.ANSWER_2)
        answer_3_text = self.get_text(*ExamCheckAnswersPageLocators.ANSWER_3)
        correct_color = "#16a085"
        wrong_color = "#ff0000"
        selected_info = " (Zaznaczona odpowiedź)"
        if correct_answer in ("A", "T"):
            if not answer_1_color == correct_color:
                return False
        elif correct_answer in ("B", "N"):
            if not answer_2_color == correct_color:
                return False
        elif correct_answer == "C":
            if not answer_3_color == correct_color:
                return False
        else:
            return False

        if not correct_answer == selected_answer:
            if selected_answer in ("A", "T"):
                if not answer_1_color == wrong_color and not answer_1_text[-23:] == selected_info:
                    return False
            elif selected_answer in ("B", "N"):
                if not answer_2_color == wrong_color and not answer_2_text[-23:] == selected_info:
                    return False
            elif selected_answer == "C":
                if not answer_3_color == wrong_color and not answer_3_text[-23:] == selected_info:
                    return False
            else:
                return False
        return True

    def button_third_displayed(self):
        return self.get_attributes(*ExamCheckAnswersPageLocators.ANSWER_3)["displayed"]

    def is_question_menu_colored(self, selected_answers, correct_answers):
        correct_color = "16a085"
        wrong_color = "#ff0000"
        for i in range(32):
            question_color = Color.from_string(
                self.get_attributes(*ExamCheckAnswersPageLocators.QUESTIONS[i])['background-color']).hex
            if selected_answers[i] == correct_answers[i]:
                if not question_color == correct_color:
                    return False
            else:
                if not question_color == wrong_color:
                    return False
        return True

    def next_question(self, iterator):
        if iterator < 31:
            self.click_button(*ExamCheckAnswersPageLocators.QUESTIONS[iterator + 1])

    def title(self):
        return self.is_title_matches("Odpowiedzi z egzaminu")