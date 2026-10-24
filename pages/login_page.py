# https://stepik.org/lesson/199980 — пишем первые тесты с помощью Page Object
# https://stepik.org/lesson/201964/step/12 — группировка тестов: setup (регистрация)
import time

from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    """Страница логина/регистрации."""

    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert "login" in self.browser.current_url, \
            f"URL не содержит 'login': {self.browser.current_url}"

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), \
            "Форма логина не представлена"

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), \
            "Форма регистрации не представлена"

    def register_new_user(self):
        """Регистрирует нового пользователя со случайным email."""
        email = str(time.time()) + "@fakemail.org"
        password = "Qwerty123"
        self.browser.find_element(
            *LoginPageLocators.REGISTRATION_EMAIL
        ).send_keys(email)
        self.browser.find_element(
            *LoginPageLocators.REGISTRATION_PASSWORD1
        ).send_keys(password)
        self.browser.find_element(
            *LoginPageLocators.REGISTRATION_PASSWORD2
        ).send_keys(password)
        self.browser.find_element(
            *LoginPageLocators.REGISTRATION_BUTTON
        ).click()
