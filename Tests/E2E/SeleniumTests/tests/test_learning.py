from src.test_base.web_driver_setup import BaseTest
from src.pages import login, prepare_learning, learning, navigation_bar
from src.test_base import test_data
from src.test_base.database import Database


class Exam(BaseTest):
    def setUp(self):
        super().setUp()
        login_page = login.LoginPage(self.driver)
        self.prepare_learning_page = prepare_learning.PrepareLearningPage(self.driver)
        self.learning_page = learning.LearningPage(self.driver)
        self.navigation = navigation_bar.NavigationBar(self.driver)
        login_page.login()
        self.navigation.go_to_prepare_learning()
        self.prepare_learning_page.reset_progress("B", "1")
        self.prepare_learning_page.prepare_learning_b_module_1()
        self.assertTrue(self.learning_page.title())
        self.db = Database()

    def test_17_learning_category_b_module_1(self):
        category = "B"
        module = "W1"
        question = self.db.get_questions(category, module)[0]

        media = question[2]
        self.assertEqual(self.learning_page.get_category(), category)
        self.assertEqual(self.learning_page.get_question_number(), "1")
        self.assertEqual(self.learning_page.get_source(), question[3].replace("  ", " ").strip())
        if media[-3:] == 'mp4':
            self.assertEqual(self.learning_page.get_video_attributes()["src"],  test_data.APP_URL + "static/enpj/media/" + media)
            self.assertFalse(self.learning_page.get_image_attributes()["displayed"])
            self.assertTrue(self.learning_page.get_video_attributes()["displayed"])
        elif media[-3:].lower() == 'jpg':
            self.assertEqual(self.learning_page.get_image_attributes()["src"],  test_data.APP_URL + "static/enpj/media/" + media)
            self.assertTrue(self.learning_page.get_image_attributes()["displayed"])
            self.assertFalse(self.learning_page.get_video_attributes()["displayed"])
        else:
            self.assertEqual(self.learning_page.get_image_attributes()["src"],  test_data.APP_URL + "static/enpj/media/brak_zdjecia_1024x576.jpg")
            self.assertTrue(self.learning_page.get_image_attributes()["displayed"])
            self.assertFalse(self.learning_page.get_video_attributes()["displayed"])

        self.assertEqual(self.learning_page.get_question(), question[0].replace("  ", " ").strip())
        self.learning_page.take_answer_t()
        if question[1] == "T":
            self.assertTrue(self.learning_page.is_answer_t_correct())
        else:
            self.assertFalse(self.learning_page.is_answer_t_correct())
            self.assertTrue(self.learning_page.is_answer_n_correct())

    def test_18_learning_deleted_cookies(self):
        self.learning_page.next_question()
        self.assertEqual(self.learning_page.get_question_number(), "2")
        self.navigation.go_to_prepare_learning()
        self.prepare_learning_page.reset_progress("B", "1")
        self.prepare_learning_page.prepare_learning_b_module_1()
        self.assertEqual(self.learning_page.get_question_number(), "1")

    def test_19_learning_continue(self):
        self.learning_page.next_question()
        self.assertEqual(self.learning_page.get_question_number(), "2")
        self.navigation.go_to_prepare_learning()
        self.prepare_learning_page.prepare_learning_b_module_1()
        self.assertEqual(self.learning_page.get_question_number(), "2")
