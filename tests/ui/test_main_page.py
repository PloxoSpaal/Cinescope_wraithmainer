import time
from playwright.sync_api import sync_playwright
from ui.main_page import MainPage
from utils.data_generator import DataGenerator as DG
import pytest
import allure


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Main")
@pytest.mark.ui
class TestMainPage:
    @allure.title("Проведение успешного перехода на страницу фильмов")
    def test_redirect_to_movies_page(self, main_page: MainPage):
        main_page.open_main_page()
        main_page.click_load_button()
        main_page.assert_was_redirect_to_movies_page()
        time.sleep(5)
