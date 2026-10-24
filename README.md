# Финальный проект курса: автотесты магазина (Page Object Model)

Итоговый тестовый проект курса Stepik
[«Автоматизация тестирования с помощью Selenium и Python»](https://stepik.org/course/575)
(урок [4.3 «Улучшаем дизайн тестов», финальное задание](https://stepik.org/lesson/201964/step/15)).

Тесты проверяют интернет-магазин [selenium1py.pythonanywhere.com](http://selenium1py.pythonanywhere.com/)
с помощью Python + Selenium + PyTest.

**Проверялось на:** Windows 11, Python 3.12, Google Chrome.

## Структура проекта

```
stepik_final_test/          # корень репозитория
├── __init__.py              # делает корень пакетом (относительные импорты)
├── conftest.py              # фикстура browser + опции --browser_name, --language
├── pytest.ini               # маркер need_review
├── requirements.txt         # зависимости
├── test_main_page.py        # тесты главной страницы
├── test_product_page.py     # тесты страницы товара (включая класс с setup)
└── pages/                   # Page Object
    ├── __init__.py
    ├── base_page.py         # базовый класс: ожидания, отрицательные проверки
    ├── locators.py          # все локаторы по страницам
    ├── main_page.py         # главная страница
    ├── login_page.py        # логин/регистрация
    ├── product_page.py      # страница товара
    └── basket_page.py       # корзина
```

## Как запустить

```bash
pip install -r requirements.txt
pytest -v --tb=line --language=en -m need_review
```

Тесты также запускаются без маркера и с выбором браузера:

```bash
pytest -v --tb=line --language=ru --browser_name=firefox
pytest test_product_page.py -k offer0
```

Нужен установленный Google Chrome (или Firefox) и chromedriver/geckodriver в PATH.
Новый пользователь для тестов регистрируется в `setup` со случайным email,
поэтому тесты не зависят от состояния магазина между запусками.

## Какие приёмы курса применены

| Приём | Где в коде | Шаг курса |
|---|---|---|
| Page Object Model | `pages/` — каждая страница своим классом | 4.1–4.2 |
| Наследование: все страницы наследуют `BasePage` | `pages/*.py` | 4.3, шаги 7–9 |
| Независимость от данных: `pytest.mark.parametrize` по 10 промо-ссылкам | `test_product_page.py` | 4.3, шаг 3 |
| Независимость от контента: имя товара и цена берутся со страницы | `ProductPage.should_be_product_name_in_success_message` | 4.3, шаг 4 |
| Известный баг: промо `offer6` помечен `xfail` | `test_product_page.py` | 4.3, шаг 4 |
| Отрицательные проверки: `is_not_element_present`, `is_element_disappeared` | `pages/base_page.py`, тесты `test_guest_cant_see_success_message_*` | 4.3, шаги 5–6 |
| Группировка тестов: `TestUserAddToBasketFromProductPage` + `setup` с регистрацией | `test_product_page.py` | 4.3, шаги 11–13 |

Все локаторы вынесены в `pages/locators.py`, в теле тестов нет `assert` —
все проверки и действия инкапсулированы в методах PageObject.

## Ссылки на задания курса

- [2.1–2.4 — задачи модуля 2 (module2/)](https://github.com/noisebac/autotests_selenium_py/tree/main/module2)
- [3.6 — параметризация и фикстуры PyTest (3_6_10/)](https://github.com/noisebac/autotests_selenium_py/tree/main/3_6_10)
- 4.1–4.3 — Page Object, отрицательные проверки, наследование, setup: этот проект
