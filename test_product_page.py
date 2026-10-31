# https://stepik.org/lesson/201964/step/2 — задание: добавление в корзину со страницы товара
# https://stepik.org/lesson/201964/step/3 — независимость от данных
# https://stepik.org/lesson/201964/step/4 — независимость от контента, ищем баг
# https://stepik.org/lesson/201964/step/6 — отрицательные проверки
# https://stepik.org/lesson/201964/step/9 — наследование
# https://stepik.org/lesson/201964/step/12 — группировка тестов: setup
import pytest

from pages.product_page import ProductPage
from pages.basket_page import BasketPage

base_link = "http://selenium1py.pythonanywhere.com/catalogue/coders-at-work_207/"

# Независимость от данных: параметризация промо-ссылок.
# Раньше offer6 был помечен xfail как сломанный промо на сервере, но в текущих
# прогонах он проходит (XPASS), а падает — без предсказуемости — то offer7, то
# сетевые таймауты. Баг на демо-сайте подвижный, поэтому номер не закрепляем.
promo_links = [f"{base_link}?promo=offer{n}" for n in range(10)]


@pytest.mark.need_review
@pytest.mark.parametrize("promo_link", promo_links)
def test_guest_can_add_product_to_basket(browser, promo_link):
    """Гость может добавить товар в корзину с промо-страницы товара."""
    page = ProductPage(browser, promo_link)
    page.open()
    page.add_product_to_cart()
    page.solve_quiz_and_get_code()
    page.should_be_product_added_to_basket()


@pytest.mark.need_review
def test_guest_cant_see_product_in_basket_opened_from_product_page(browser):
    """Корзина пуста, если гость открыл её со страницы товара."""
    page = ProductPage(browser, base_link)
    page.open()
    page.go_to_basket()
    basket_page = BasketPage(browser, browser.current_url)
    basket_page.should_be_empty_basket()


@pytest.mark.need_review
def test_guest_can_go_to_login_page_from_product_page(browser):
    """Гость может перейти на страницу логина со страницы товара."""
    page = ProductPage(browser, base_link)
    page.open()
    login_page = page.go_to_login_page()
    login_page.should_be_login_page()


@pytest.mark.need_review
@pytest.mark.xfail(
    reason="сервер показывает сообщение об успехе сразу после добавления",
    strict=False,
)
def test_guest_cant_see_success_message_after_adding_product_to_cart(browser):
    """Сообщение об успехе отсутствует сразу после добавления (отрицательная проверка).

    ``base_link`` ведёт на обычную страницу товара без ``?promo=``, поэтому
    капчи в alert здесь нет и ``solve_quiz_and_get_code()`` не вызывается:
    он ждал бы алерт, который никогда не появится.
    """
    page = ProductPage(browser, base_link)
    page.open()
    page.add_product_to_cart()
    page.should_not_be_success_message()


def test_guest_cant_see_success_message_before_adding_product_to_cart(browser):
    """Сообщение об успехе отсутствует, пока товар не добавили (отрицательная проверка)."""
    page = ProductPage(browser, base_link)
    page.open()
    page.should_not_be_success_message()


class TestUserAddToBasketFromProductPage:
    """Тесты для зарегистрированного пользователя: регистрация выполняется в setup."""

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, browser):
        """Setup: открываем страницу товара, регистрируем нового пользователя."""
        page = ProductPage(browser, base_link)
        page.open()
        page.should_be_login_link()
        login_page = page.go_to_login_page()
        login_page.should_be_login_page()
        login_page.register_new_user()
        # should_be_authorized_user() дополнительно проверяет сообщение
        # «Thanks for registering!» — так сбой называет свою причину.
        login_page.should_be_authorized_user()

    @pytest.mark.need_review
    def test_user_can_add_product_to_basket(self, browser):
        """Зарегистрированный пользователь может добавить товар в корзину."""
        page = ProductPage(browser, base_link)
        page.open()
        page.add_product_to_cart()
        page.should_be_product_added_to_basket()

    def test_user_cant_see_success_message(self, browser):
        """Зарегистрированный пользователь не видит сообщение об успехе до добавления."""
        page = ProductPage(browser, base_link)
        page.open()
        page.should_not_be_success_message()
