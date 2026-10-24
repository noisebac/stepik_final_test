# https://stepik.org/lesson/201964/step/2 — задание: добавление в корзину со страницы товара
import math

from selenium.common.exceptions import NoAlertPresentException

from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):
    """Страница товара."""

    def add_product_to_cart(self):
        button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        button.click()

    def solve_quiz_and_get_code(self):
        """Решаем математическую капчу в alert и возвращаем код подтверждения."""
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(int(x))))))
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

    def get_product_name(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_NAME).text

    def get_product_price(self):
        return self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE).text

    # --- проверки успешного добавления в корзину ---

    def should_be_product_name_in_success_message(self):
        """Имя товара в сообщении об успехе совпадает с именем на странице."""
        product_name = self.get_product_name()
        messages = self.browser.find_elements(
            *ProductPageLocators.PRODUCT_IN_BASKET_MESSAGE
        )
        assert any(
            product_name in message.text for message in messages
        ), f"Сообщение не содержит имя товара '{product_name}'"

    def should_be_basket_total(self):
        """Сумма корзины равна цене товара."""
        product_price = self.get_product_price()
        basket_total = self.browser.find_element(
            *ProductPageLocators.BASKET_TOTAL
        ).text
        assert product_price == basket_total, (
            f"Сумма корзины '{basket_total}' не совпадает с ценой '{product_price}'"
        )

    # --- отрицательные проверки (курс 4.3, отрицательные проверки) ---

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Сообщение об успехе присутствует, хотя не должно"

    def should_be_success_message_disappeared(self):
        assert self.is_element_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), \
            "Сообщение об успехе не исчезло, хотя должно"
