# https://stepik.org/lesson/201964/step/5 — отрицательные проверки
import math

from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .locators import BasePageLocators


class BasePage:
    """Базовый класс страницы: держит browser и url, содержит общие методы."""

    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def solve_quiz_and_get_code(self):
        """Решаем математическую капчу в alert и возвращаем код подтверждения."""
        # Без явного ожидания switch_to.alert бросает NoAlertPresentException,
        # если алерт появляется не мгновенно после клика.
        WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        # float, а не int: значение в алерте может быть дробным.
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
            return alert_text
        except NoAlertPresentException:
            print("No second alert")
            return None

    def is_element_present(self, how, what):
        """Элемент присутствует на странице прямо сейчас."""
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        """Элемент НЕ появился за отведённое время (отрицательная проверка)."""
        try:
            WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return True
        return False

    def is_element_disappeared(self, how, what, timeout=4):
        """Элемент исчез за отведённое время (отрицательная проверка)."""
        try:
            WebDriverWait(self.browser, timeout).until_not(
                EC.presence_of_element_located((how, what))
            )
        except TimeoutException:
            return False
        return True

    def go_to_basket(self):
        basket_link = self.browser.find_element(*BasePageLocators.BASKET_LINK)
        basket_link.click()

    def go_to_login_page(self):
        login_link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        login_link.click()
        # Импорт внутри метода: login_page импортирует base_page на уровне
        # модуля, и наружный импорт дал бы циклическое замыкание.
        from .login_page import LoginPage
        return LoginPage(browser=self.browser, url=self.browser.current_url)

    def should_be_login_link(self):
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), \
            "Ссылка на логин не представлена на странице"

    def should_be_authorized_user(self):
        assert self.is_element_present(*BasePageLocators.USER_ICON), \
            "Пользователь не авторизован: иконки профиля нет на странице"
