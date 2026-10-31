# https://stepik.org/lesson/199980 — пишем первые тесты с помощью Page Object
from .base_page import BasePage
from .locators import MainPageLocators


class MainPage(BasePage):
    """Главная страница магазина.

    ``go_to_login_page`` унаследован от ``BasePage`` — он возвращает
    экземпляр ``LoginPage``, поэтому отдельное переопределение здесь не нужно.
    """

    def should_be_login_link(self):
        assert self.is_element_present(*MainPageLocators.LOGIN_LINK), \
            "Ссылка на логин не представлена на главной странице"
