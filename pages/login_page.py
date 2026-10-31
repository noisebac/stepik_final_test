# https://stepik.org/lesson/199980 — пишем первые тесты с помощью Page Object
# https://stepik.org/lesson/201964/step/12 — группировка тестов: setup (регистрация)
import secrets
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from .locators import BasePageLocators, LoginPageLocators


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
        """Регистрирует нового пользователя со случайными email и паролем.

        Пароль тоже делаем случайным: демо-сайт отклоняет типовые значения из
        списка обычных паролей (например, "Qwerty123"), аккаунт не создаётся,
        и тест падает в setup с «пользователь не авторизован».
        """
        email = f"{time.time()}@fakemail.org"
        password = secrets.token_urlsafe(12)
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
        # Явно ждём исхода регистрации. Если сайт отклонит данные, мы сразу
        # увидим сообщение об ошибке вместо отвлечённого «иконки нет».
        WebDriverWait(self.browser, 10).until(
            EC.any_of(
                EC.presence_of_element_located(BasePageLocators.USER_ICON),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "#register_form .alert-danger, .alert-danger")
                ),
            )
        )
        errors = self.browser.find_elements(
            By.CSS_SELECTOR, "#register_form .alert-danger, .alert-danger"
        )
        if errors:
            raise AssertionError(
                "Регистрация отклонена сайтом: " + errors[0].text.strip()
            )

    def should_be_registration_success(self):
        """Сайт подтвердил регистрацию сообщением «Thanks for registering!»."""
        assert self.is_element_present(
            *LoginPageLocators.REGISTRATION_SUCCESS_MESSAGE
        ), "Сообщение об успешной регистрации не появилось"

    def should_be_authorized_user(self):
        """Составная проверка: регистрация подтверждена и пользователь вошёл."""
        self.should_be_registration_success()
        super().should_be_authorized_user()
