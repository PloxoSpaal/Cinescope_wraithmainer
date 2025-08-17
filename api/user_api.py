from custom_requester.custom_requester import CustomRequester
from requests import Response
from schemas.user_schema import CreateUserRequestSchema
from constants import AUTH_BASE_URL
import allure


class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    @allure.step("Получение пользователя /user/{user_locator}")
    def get_user(self, user_locator: str, expected_status=200) -> Response:
        """
        Получение данных пользователя по локатору
        :param user_locator: ID или email пользователя
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request("GET", f"/user/{user_locator}", expected_status=expected_status)

    def get_user_info(self, user_id: str, expected_status=200) -> Response:
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    @allure.step("Создание пользователя /user")
    def create_user(self, user_data: CreateUserRequestSchema, expected_status=201) -> Response:
        """
        Метод создания пользователя
        :param user_data: Информация пользователя
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    @allure.step("Удаление пользователя /user/{user_id}")
    def delete_user(self, user_id: str, expected_status=204) -> Response:
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )
