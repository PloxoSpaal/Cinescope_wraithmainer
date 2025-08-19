import allure
from playwright.sync_api import Page
from ui.base_page import BasePage


class MainPage(BasePage):
    """
    Класс MainPage для описания главной страницы
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.home_url

        self.login_link = page.get_by_role("button", name="Войти")
        self.text = page.get_by_role("heading", name="Последние фильмы")
        self.load_button = page.get_by_role("button", name="Показать еще")
        self.movie_cards = page.locator('.rounded-xl')
        self.movie_text = page.locator('.text-md')
        self.movie_images = page.get_by_role('img')
        self.movies_bottoms_text = page.locator('p.truncate')
        self.movie_button = page.get_by_role('button', name='Подробнее')

    @allure.step('Открытие главной страницы')
    def open_main_page(self):
        self.open_url(self.url)

    @allure.step('Клик по кнопке "Показать ещё"')
    def click_load_button(self):
        self.load_button.click()

    @allure.step('Проверка редиректа на страницу фильмов')
    def assert_was_redirect_to_movies_page(self):
        self.wait_redirect_for_url(f"{self.home_url}movies")