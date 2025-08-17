import time
from playwright.sync_api import sync_playwright
from ui.register_page import RegisterPage
from utils.data_generator import DataGenerator as DG
import pytest
import allure


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_registration_register_page(self, register_page: RegisterPage):
        fio = DG.generate_random_name()
        email = DG.generate_random_email()
        password = DG.generate_random_password()
        repeat_password = password
        register_page.open_register_page()
        register_page.register(
            fio=fio, email=email, password=password, repeat_password=repeat_password)
        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()

    @allure.title("Проведение неуспешной регистрации")
    def test_error_registration_register_page(self, register_page: RegisterPage):
        fio = DG.generate_random_name()
        email = DG.generate_random_email()+'@'
        password = DG.generate_random_password()
        repeat_password = password
        register_page.open_register_page()
        register_page.register(
            fio=fio, email=email, password=password, repeat_password=repeat_password)
        register_page.make_screenshot_and_attach_to_allure()