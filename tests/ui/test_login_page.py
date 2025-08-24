import time
from playwright.sync_api import sync_playwright
from pytest_check import check

from ui.login_page import LoginPage
from utils.data_generator import DataGenerator as DG
import pytest
import allure


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_user_login_page(self, login_page: LoginPage, registered_user):
        login_page.open_login_page()
        login_page.login_user(email=registered_user.email, password=registered_user.password)
        with check:
            login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_allert_was_pop_up()

    @allure.title("Проведение неуспешного входа в систему")
    def test_login_with_error_user_login_page(self, login_page: LoginPage, registered_user):
        login_page.open_login_page()
        login_page.login_user(email=registered_user.email, password=registered_user.password+'123')
        with check:
            login_page.assert_allert_error_pop_up()
        login_page.make_screenshot_and_attach_to_allure()
