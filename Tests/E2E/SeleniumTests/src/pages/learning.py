from src.locators import LearningPageLocators
from src.pages.base import BasePage
from selenium.webdriver.support.color import Color

class LearningPage(BasePage):
    def get_category(self):
        return self.get_text(*LearningPageLocators.CATEGORY_B)

    def get_question_number(self):
        return self.get_text(*LearningPageLocators.QUESTION_NUMBER)

    def get_image_attributes(self):
        return self.get_attributes(*LearningPageLocators.IMAGE, src=True)

    def get_video_attributes(self):
        return self.get_attributes(*LearningPageLocators.VIDEO, src=True)

    def get_question(self):
        return self.get_text(*LearningPageLocators.QUESTION)

    def take_answer_t(self):
        self.click_button(*LearningPageLocators.ANSWER_T)

    def get_source(self):
        return self.get_text(*LearningPageLocators.SOURCE)

    def is_answer_t_correct(self):
        color = Color.from_string(
            self.get_attributes(*LearningPageLocators.ANSWER_T)['background-color']).hex
        return color == "#008000"

    def is_answer_n_correct(self):
        color = Color.from_string(
            self.get_attributes(*LearningPageLocators.ANSWER_N)['background-color']).hex
        return color == "#008000"

    def next_question(self):
        self.click_button(*LearningPageLocators.NEXT)

    def title(self):
        return self.is_title_matches("Nauka")