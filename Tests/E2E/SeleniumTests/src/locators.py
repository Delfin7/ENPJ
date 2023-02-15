from selenium.webdriver.common.by import By


class NavigationBarLocators(object):
    LOGIN = (By.CSS_SELECTOR, "a[href='/login/']")
    SIGNUP = (By.CSS_SELECTOR, "a[href='/signup/']")
    PREPARE_LEARNING = (By.CSS_SELECTOR, "a[href='prepare-learning']")
    PREPARE_EXAM = (By.CSS_SELECTOR, "a[href='/']")
    STATISTICS = (By.CSS_SELECTOR, "a[href='statistics']")
    OPTIONS = (By.CSS_SELECTOR, "a[href='options']")
    LOGOUT = (By.CSS_SELECTOR, "a[href='logout']")


class LoginPageLocators(object):
    LOGIN = (By.ID, 'id_login')
    PASSWORD = (By.ID, "id_password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    INCORRECT_EMAIL = (By.XPATH, "//li[normalize-space()='Enter a valid email address.']")
    NON_EXISTENT_ACCOUNT = (By.XPATH, "//li[contains(text(),'The e-mail address and/or password you specified a')]")


class SignupPageLocators(object):
    EMAIL = (By.ID, 'id_email')
    USERNAME = (By.ID, 'id_username')
    PASSWORD = (By.ID, "id_password1")
    PASSWORD_CONFIRM = (By.ID, "id_password2")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    INCORRECT_EMAIL = (By.XPATH, "//li[normalize-space()='Enter a valid email address.']")
    INCORRECT_PASSWORD = (By.XPATH, "//li[contains(text(),'This password is too short. It must contain at lea')]")
    NOT_SAME_PASSWORD = (By.XPATH, "//li[normalize-space()='You must type the same password each time.']")
    EXISTING_EMAIL = (By.XPATH, "//li[contains(text(),'A user is already registered with this e-mail addr')]")
    EXISTING_USERNAME = (By.XPATH, "//li[normalize-space()='A user with that username already exists.']")


class OptionsPageLocators(object):
    LANGUAGE = (By.ID, 'language')
    SIGN_LANGUAGE = (By.ID, "signLanguage")
    SAVE = (By.CSS_SELECTOR, "button[onclick='save()']")
    CHANGE_PASSWORD = (By.XPATH, "//button[contains(text(),'Zmiana hasła')]")
    OPTIONS_SAVED = (By.ID, "info")


class ChangePasswordPageLocators(object):
    CURRENT_PASSWORD = (By.ID, "id_oldpassword")
    NEW_PASSWORD = (By.ID, "id_password1")
    NEW_PASSWORD_CONFIRM = (By.ID, "id_password2")
    SUBMIT = (By.CSS_SELECTOR, "button[name='action']")

    PASSWORD_CHANGED = (By.XPATH, "//b[normalize-space()='Password successfully changed.']")
    INCORRECT_CURRENT_PASSWORD = (By.XPATH, "//li[normalize-space()='Please type your current password.']")
    INCORRECT_NEW_PASSWORD = (By.XPATH, "//li[contains(text(),'This password is too short. It must contain at least 8 characters.')]")
    INCORRECT_NEW_PASSWORD2 = (By.XPATH, "//li[normalize-space()='This password is too common.']")


class PrepareExamPageLocators(object):
    CATEGORY_B = (By.CSS_SELECTOR, """button[onclick="takeExam('B')"]""")
    CONTINUE_CHECK_EXAM = (By.ID, "buttonContinue")


class ExamPageLocators(object):
    POINTS = (By.ID, "points")
    CATEGORY = (By.XPATH, "//span[normalize-space()='B']")
    IMAGE = (By.ID, "img")
    VIDEO = (By.ID, "video")
    QUESTION = (By.ID, "question")
    ANSWER_T = (By.ID, "buttonT")
    ANSWER_N = (By.ID, "buttonN")
    ANSWER_A = (By.ID, "buttonA")
    ANSWER_B = (By.ID, "buttonB")
    ANSWER_C = (By.ID, "buttonC")
    FINISH = (By.ID, "buttonZakoncz")
    PRIMARY_NUMBER = (By.ID, "primary_number")
    SPEC_NUMBER = (By.ID, "spec_number")
    NEXT_QUESTION = (By.ID, "buttonNastepnePytanie")
    START_VIDEO = (By.CSS_SELECTOR, "button[onclick='startButton()']")


class ExamResultPageLocators(object):
    CHECK_ANSWERS = (By.XPATH, "//button[contains(text(),'Sprawdź odpowiedzi')]")
    FINISHED_EXAM = (By.XPATH, "//h1[contains(text(),'Zakończyłeś egzamin')]")
    CATEGORY = (By.XPATH, "//p[contains(text(),'Kategoria')]")
    RESULT = (By.XPATH, "//p[contains(text(),'Uzyskałeś wynik')]")


class ExamCheckAnswersPageLocators(object):
    POINTS = (By.ID, "points")
    CATEGORY = (By.XPATH, "//span[normalize-space()='B']")
    IMAGE = (By.ID, "img")
    VIDEO = (By.ID, "video")
    QUESTION = (By.ID, "question")
    ANSWER_1 = (By.ID, "button1")
    ANSWER_2 = (By.ID, "button2")
    ANSWER_3 = (By.ID, "button3")
    QUESTIONS = [(By.ID, "q" + str(i)) for i in range(1, 33)]


class PrepareLearningPageLocators(object):
    CATEGORY_B = (By.CSS_SELECTOR, """button[onclick="chooseModule('B')"]""")
    MODULE_FIRST = (By.ID, "r1")


class LearningPageLocators(object):
    IMAGE = (By.ID, "img")
    VIDEO = (By.ID, "video")
    QUESTION = (By.ID, "question")
    ANSWER_T = (By.ID, "buttonT")
    ANSWER_N = (By.ID, "buttonN")
    CATEGORY_B = (By.XPATH, "//td[normalize-space()='B']")
    QUESTION_NUMBER = (By.ID, "questionNumber")
    INPUT_QUESTION_NUMBER = (By.ID, "inputQuestionNumber")
    CONFIRM = (By.CSS_SELECTOR, "button[onclick='confirm()']")
    PREVIOUS = (By.ID, "prev")
    NEXT = (By.ID, "next")
    SOURCE = (By.ID, "source")