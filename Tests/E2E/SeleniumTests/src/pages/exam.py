from src.locators import ExamPageLocators
from src.pages.base import BasePage


class ExamPage(BasePage):
    def get_points(self):
        return self.get_text(*ExamPageLocators.POINTS)

    def get_category(self):
        return self.get_text(*ExamPageLocators.CATEGORY)

    def get_image_attributes(self):
        return self.get_attributes(*ExamPageLocators.IMAGE, src=True)

    def get_video_attributes(self):
        return self.get_attributes(*ExamPageLocators.VIDEO, src=True)

    def get_question(self):
        return self.get_text(*ExamPageLocators.QUESTION)

    def button_t_displayed(self):
        return self.get_attributes(*ExamPageLocators.ANSWER_T)["displayed"]

    def button_n_displayed(self):
        return self.get_attributes(*ExamPageLocators.ANSWER_N)["displayed"]

    def button_a_displayed(self):
        return self.get_attributes(*ExamPageLocators.ANSWER_A)["displayed"]

    def button_b_displayed(self):
        return self.get_attributes(*ExamPageLocators.ANSWER_B)["displayed"]

    def button_c_displayed(self):
        return self.get_attributes(*ExamPageLocators.ANSWER_C)["displayed"]

    def start_video(self):
        self.click_button(*ExamPageLocators.START_VIDEO)

    def take_answer_t(self):
        self.click_button(*ExamPageLocators.ANSWER_T)

    def take_answer_a(self):
        self.click_button(*ExamPageLocators.ANSWER_A)

    def next_question(self):
        self.click_button(*ExamPageLocators.NEXT_QUESTION)

    def finish_exam(self):
        self.click_button(*ExamPageLocators.FINISH)

    def next_question_button_displayed(self):
        return self.get_attributes(*ExamPageLocators.NEXT_QUESTION)["displayed"]

    def title(self):
        return self.is_title_matches("Egzamin")