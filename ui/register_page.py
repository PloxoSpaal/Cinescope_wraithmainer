from playwright.sync_api import Page
from ui.base_page import BasePage


class RegisterPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}/register"

        self.fio_input = page.get_by_role('textbox', name='Имя Фамилия Отчество')
        self.email_input = page.get_by_role('textbox', name='Email')
        self.password_input = page.get_by_role('textbox', name='Пароль', exact=True)
        self.repeat_password_input = page.get_by_role('textbox', name='Повторите пароль')

        self.register_btn = page.get_by_role('button', name='Зарегистрироваться')
        self.login_link = page.get_by_role('link', name='Войти')

    def open_register_page(self):
        self.open_url(self.url)

    def click_register_button(self):
        self.register_btn.click()

    def click_login_link(self):
        self.login_link.click()

    def enter_fio(self, value: str):
        self.fio_input.fill(value=value)

    def enter_email(self, email: str):
        self.email_input.fill(value=email)

    def enter_password(self, password: str):
        self.password_input.fill(value=password)

    def enter_repeat_password(self, repeat_password: str):
        self.repeat_password_input.fill(value=repeat_password)

    def register(self, fio: str, email: str, password: str, repeat_password: str):
        self.enter_fio(fio)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_repeat_password(repeat_password)
        self.click_register_button()

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")

