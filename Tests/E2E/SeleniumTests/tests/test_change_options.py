from src.test_base.web_driver_setup import BaseTest
from src.pages import login, navigation_bar, options


class ChangeOptions(BaseTest):
    def setUp(self):
        super().setUp()
        navigation = navigation_bar.NavigationBar(self.driver)
        login_page = login.LoginPage(self.driver)
        self.options_page = options.OptionsPage(self.driver)
        login_page.login()
        navigation.go_to_options()
        self.options_page.set_language_polish()
        self.options_page.uncheck_sign_language()
        self.options_page.save()
        navigation.go_to_options()
        self.assertTrue(self.options_page.title())

    def test_14_change_language(self):
        self.options_page.set_language_english()
        self.options_page.save()
        self.assertTrue(self.options_page.is_saved())

    def test_15_not_change_language_and_sing_language(self):
        self.options_page.save()
        self.assertFalse(self.options_page.is_saved())

    def test_16_change_sign_language(self):
        self.options_page.check_sign_language()
        self.options_page.save()
        self.assertTrue(self.options_page.is_saved())

    def tearDown(self):
        self.options_page.set_language_polish()
        self.options_page.uncheck_sign_language()
        self.options_page.save()
        super().tearDown()