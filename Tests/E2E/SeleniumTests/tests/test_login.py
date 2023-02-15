from src.pages import login, prepare_exam, navigation_bar
from src.test_base.web_driver_setup import BaseTest


class Login(BaseTest):
    def setUp(self):
        super().setUp()
        self.login_page = login.LoginPage(self.driver)

    def test_4_login(self):
        prepare_exam_page = prepare_exam.PrepareExamPage(self.driver)
        self.login_page.login()
        self.assertTrue(prepare_exam_page.title())

    def test_5_login_invalid_email(self):
        self.login_page.login("bademail@t", "password")
        self.assertTrue(self.login_page.is_title_matches("Logowanie"))
        self.assertTrue(self.login_page.is_incorrect_email())

    def test_6_login_non_existent_account(self):
        self.login_page.login("non_existent_login@xd.xd", "non_existent_password")
        self.assertTrue(self.login_page.is_title_matches("Logowanie"))
        self.assertTrue(self.login_page.is_non_existent_account())

    def test_7_logout(self):
        navigation = navigation_bar.NavigationBar(self.driver)
        self.login_page.login()
        navigation.logout()
        self.login_page.title()

