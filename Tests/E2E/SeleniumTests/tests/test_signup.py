from src.test_base.web_driver_setup import BaseTest
from src.pages import signup, navigation_bar, prepare_exam
from src.test_base.database import Database
from src.test_base import test_data


class Signup(BaseTest):
    def setUp(self):
        super().setUp()
        navigation = navigation_bar.NavigationBar(self.driver)
        self.signup_page = signup.SignupPage(self.driver)
        navigation.go_to_signup()

    def test_1_signup(self):
        prepare_exam_page = prepare_exam.PrepareExamPage(self.driver)
        db = Database()
        self.signup_page.signup("emailTestowy@test.pl", "testUser", "testpassword", "testpassword")
        self.assertTrue(prepare_exam_page.title())
        db.delete_user("emailTestowy@test.pl")

    def test_2_signup_invalid_email_password_confirm_password(self):
        self.signup_page.signup("test@t", "test", "test", "test")
        self.assertTrue(self.signup_page.title())
        self.assertTrue(self.signup_page.is_incorrect_email())
        self.assertTrue(self.signup_page.is_incorrect_password())
        self.signup_page.signup("", "", "test123456", "test654321")
        self.assertTrue(self.signup_page.title())
        self.assertTrue(self.signup_page.is_incorrect_email())
        self.assertTrue(self.signup_page.is_not_same_password())

    def test_3_signup_existing_email_username(self):
        self.signup_page.signup(test_data.EMAIL, test_data.USERNAME, "testpassword", "testpassword")
        self.assertTrue(self.signup_page.title())
        self.assertTrue(self.signup_page.is_existing_email())
        self.assertTrue(self.signup_page.is_existing_username())