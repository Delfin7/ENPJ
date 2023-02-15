from src.test_base.web_driver_setup import BaseTest
from src.pages import login, exam, prepare_exam, exam_result, exam_check_answers, navigation_bar, options
from src.test_base import test_data
from src.test_base.database import Database


class Exam(BaseTest):
    def setUp(self):
        super().setUp()
        login_page = login.LoginPage(self.driver)
        navigation = navigation_bar.NavigationBar(self.driver)
        options_page = options.OptionsPage(self.driver)
        self.prepare_exam_page = prepare_exam.PrepareExamPage(self.driver)
        self.exam_page = exam.ExamPage(self.driver)
        self.exam_result_page = exam_result.ExamResultPage(self.driver)
        login_page.login()
        navigation.go_to_options()
        options_page.set_language_polish()
        options_page.save()
        navigation.go_to_main_site()
        started_exam_exists = self.prepare_exam_page.started_exam_exists()
        self.prepare_exam_page.prepare_exam_b()
        if started_exam_exists:
            self.prepare_exam_page.alert_accept()
        self.db = Database()
        self.assertTrue(self.exam_page.title())

    def test_11_exam_category_b(self):
        category = "B"
        questions = self.db.get_exam_questions(test_data.EMAIL)
        for i in range(32):
            question = questions[i]
            media = question[5]
            self.assertEqual(self.exam_page.get_points(), str(question[6]))
            self.assertEqual(self.exam_page.get_category(), category)
            if media[-3:] == 'mp4':
                self.assertEqual(self.exam_page.get_image_attributes()["src"], test_data.APP_URL + "static/enpj/media/video-camera-2806.png")
                self.assertTrue(self.exam_page.get_image_attributes()["displayed"])
                self.assertFalse(self.exam_page.get_video_attributes()["displayed"])
                self.exam_page.start_video()
                self.assertEqual(self.exam_page.get_video_attributes()["src"],  test_data.APP_URL + "static/enpj/media/" + media)
                self.assertFalse(self.exam_page.get_image_attributes()["displayed"])
                self.assertTrue(self.exam_page.get_video_attributes()["displayed"])
            elif media[-3:].lower() == 'jpg':
                self.assertEqual(self.exam_page.get_image_attributes()["src"],  test_data.APP_URL + "static/enpj/media/" + media)
                self.assertTrue(self.exam_page.get_image_attributes()["displayed"])
                self.assertFalse(self.exam_page.get_video_attributes()["displayed"])
            else:
                self.assertEqual(self.exam_page.get_image_attributes()["src"],  test_data.APP_URL + "static/enpj/media/brak_zdjecia_1024x576.jpg")
                self.assertTrue(self.exam_page.get_image_attributes()["displayed"])
                self.assertFalse(self.exam_page.get_video_attributes()["displayed"])

            self.assertEqual(self.exam_page.get_question(), question[1].replace("  ", " ").strip())
            if i <= 19:
                self.assertTrue(self.exam_page.button_t_displayed())
                self.assertTrue(self.exam_page.button_n_displayed())
                self.assertFalse(self.exam_page.button_a_displayed())
                self.assertFalse(self.exam_page.button_b_displayed())
                self.assertFalse(self.exam_page.button_c_displayed())
                self.exam_page.take_answer_t()
                self.exam_page.next_question()
            else:
                self.assertFalse(self.exam_page.button_t_displayed())
                self.assertFalse(self.exam_page.button_n_displayed())
                self.assertTrue(self.exam_page.button_a_displayed())
                self.assertTrue(self.exam_page.button_b_displayed())
                self.assertTrue(self.exam_page.button_c_displayed())
                self.exam_page.take_answer_a()
                if i != 31:
                    self.exam_page.next_question()
                else:
                    self.assertFalse(self.exam_page.next_question_button_displayed())
                    self.exam_page.finish_exam()
                    self.exam_page.alert_accept()

        self.assertTrue(self.exam_result_page.title())
        points = self.db.get_points_from_last_exam(test_data.EMAIL)
        self.assertTrue(self.exam_result_page.check_information(category, points))

    def test_12_exam_not_all_answers_take(self):
        category = "B"
        self.exam_page.take_answer_t()
        self.exam_page.next_question()
        self.exam_page.finish_exam()
        self.exam_page.alert_accept()

        self.assertTrue(self.exam_result_page.title())
        points = self.db.get_points_from_last_exam(test_data.EMAIL)
        self.assertTrue(self.exam_result_page.check_information(category, points))

    def test_13_exam_check_answers(self):
        exam_check_answers_page = exam_check_answers.ExamCheckAnswersPage(self.driver)
        self.test_11_exam_category_b()
        self.exam_result_page.go_to_main_site()
        self.prepare_exam_page.continue_exam_check_answers()
        self.exam_result_page.check_answers()
        self.assertTrue(exam_check_answers_page.title())

        category = "B"
        questions = self.db.get_exam_questions(test_data.EMAIL)
        correct_answers = [question[7] for question in questions]
        selected_answers = [question[8] for question in questions]
        for i in range(32):
            question = questions[i]
            media = question[5]
            self.assertEqual(exam_check_answers_page.get_points(), str(question[6]))
            self.assertEqual(exam_check_answers_page.get_category(), category)
            if media[-3:] == 'mp4':
                self.assertEqual(exam_check_answers_page.get_video_attributes()["src"],
                                 test_data.APP_URL + "static/enpj/media/" + media)
                self.assertFalse(exam_check_answers_page.get_image_attributes()["displayed"])
                self.assertTrue(exam_check_answers_page.get_video_attributes()["displayed"])
            elif media[-3:].lower() == 'jpg':
                self.assertEqual(exam_check_answers_page.get_image_attributes()["src"],
                                 test_data.APP_URL + "static/enpj/media/" + media)
                self.assertTrue(exam_check_answers_page.get_image_attributes()["displayed"])
                self.assertFalse(exam_check_answers_page.get_video_attributes()["displayed"])
            else:
                self.assertEqual(exam_check_answers_page.get_image_attributes()["src"],
                                 test_data.APP_URL + "static/enpj/media/brak_zdjecia_1024x576.jpg")
                self.assertTrue(exam_check_answers_page.get_image_attributes()["displayed"])
                self.assertFalse(exam_check_answers_page.get_video_attributes()["displayed"])

            self.assertEqual(exam_check_answers_page.get_question(), question[1].replace("  ", " ").strip())
            self.assertTrue(exam_check_answers_page.check_answers(correct_answers[i], selected_answers[i]))
            if i <= 19:
                self.assertFalse(exam_check_answers_page.button_third_displayed())
            else:
                self.assertTrue(exam_check_answers_page.button_third_displayed())
            exam_check_answers_page.is_question_menu_colored(selected_answers, correct_answers)
            exam_check_answers_page.next_question(i)



