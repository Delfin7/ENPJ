from src.test_base.web_driver_setup import BaseTest
from src.pages import login, navigation_bar, options, change_password
from src.test_base import test_data


class ChangePassword(BaseTest):
    def setUp(self):
        super().setUp()
        navigation = navigation_bar.NavigationBar(self.driver)
        login_page = login.LoginPage(self.driver)
        options_page = options.OptionsPage(self.driver)
        self.change_password_page = change_password.ChangePasswordPage(self.driver)
        login_page.login()
        navigation.go_to_options()
        options_page.change_password()
        self.assertTrue(self.change_password_page.title())

    def test_8_change_password(self):
        new_password = "testpassword"
        self.change_password_page.change_password(test_data.PASSWORD, new_password, new_password)
        self.change_password_page.is_password_changed()
        self.change_password_page.change_password(new_password, test_data.PASSWORD, test_data.PASSWORD)
        self.change_password_page.is_password_changed()

    def test_9_change_password_incorrect_current_password(self):
        self.change_password_page.change_password("1", "testpassword", "testpassword")
        self.change_password_page.is_incorrect_current_password()

    def test_10_change_password_incorrect_new_password(self):
        self.change_password_page.change_password(test_data.PASSWORD, "1", "1")
        self.change_password_page.is_incorrect_new_password()