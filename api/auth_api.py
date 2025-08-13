import allure
from custom_requester.custom_requester import CustomRequester
from constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT
from requests import Session
from constants import AUTH_BASE_URL
from typing import Tuple
from requests import Response
from schemas.auth_shema import LoginRequestSchema
from schemas.user_fixture_schema import UserSchema, RegisterUserResponseSchema


class AuthAPI(CustomRequester):
    """
    Класс для работы с аутентификацией.
    """

    def __init__(self, session: Session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    @allure.step("Регистрация пользователя /register")
    def register_user(self, user_data: UserSchema, expected_status: int = 201) -> Response:
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    @allure.step("Логин пользователя /login")
    def login_user(self, login_data, expected_status: int = 200) -> Response:
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    @allure.step("Аутентификация сессии")
    def authenticate(self, user_creds: LoginRequestSchema):
        """
        Аутентификация сессии
        :param user_creds: Логин и пароль пользователя
        """
        login_data = LoginRequestSchema(**user_creds.model_dump())
        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self.update_session_headers(self.session, **{"authorization": "Bearer " + token})

    @allure.step("Разлогин сессии")
    def unauthenticate(self):
        """
        Разлогин пользователя
        """
        self.clear_session_headers(self.session)
