# https://stepik.org/lesson/201964 — задание: группировка тестов и setup
from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):
    """Страница корзины."""

    def should_be_basket_page(self):
        assert "basket" in self.browser.current_url, \
            f"URL не содержит 'basket': {self.browser.current_url}"

    def should_not_be_basket_items(self):
        assert self.is_not_element_present(*BasketPageLocators.BASKET_ITEMS), \
            "В корзине есть товары, хотя не должно быть"

    def should_be_empty_basket_message(self):
        assert self.is_element_present(*BasketPageLocators.BASKET_EMPTY_MESSAGE), \
            "Сообщение о пустой корзине отсутствует"
