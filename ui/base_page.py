from playwright.sync_api import Page
from ui.action_page import PageAction
import allure


class BasePage(PageAction):
    """
    Класс BasePage для описания базовой страницы
    """
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        # Общие локаторы для всех страниц на сайте
        self.logo_link = page.get_by_role('link', name='Cinescope')
        self.all_films_link = page.get_by_role('link', name='Все фильмы')

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.logo_link)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.all_films_link)
        self.wait_redirect_for_url(f"{self.home_url}movies")