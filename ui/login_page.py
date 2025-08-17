from playwright.sync_api import Page
from ui.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}/login"

        self.register_link = page.get_by_role('link', name='Зарегистрироваться')
        self.logo_link = page.get_by_role('link', name='Cinescope')
        self.all_films_link = page.get_by_role('link', name='Все фильмы')

        self.email_input = page.get_by_role('textbox', name='Email')
        self.password_input = page.get_by_role('textbox', name='Пароль')

        self.login_button = page.get_by_role('button', name='Войти')

    def open_login_page(self):
        self.open_url(self.url)

    def enter_email(self, email: str):
        self.email_input.fill(value=email)

    def enter_password(self, password: str):
        self.password_input.fill(value=password)

    def click_login_button(self):
        self.login_button.click()

    def click_register_link(self):
        self.register_link.click()

    def login_user(self, email: str, password: str):
        self.enter_email(email=email)
        self.enter_password(password=password)
        self.click_login_button()

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")

    def assert_allert_error_pop_up(self):
        self.check_pop_up_element_with_text("Неверная почта или пароль")