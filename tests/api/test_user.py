import pytest
import allure
from pytest_check import check

from constants import FORBIDDEN_MOVIE_ERR_MSG
from schemas.error_schema import BaseError
from schemas.user_entity_schema import User
from schemas.user_fixture_schema import UserSchema, RegisterUserResponseSchema
from schemas.user_schema import CreateUserRequestSchema


@allure.epic('Функционал взаимодействия с пользователем')
@allure.feature('Проверка функциональности создания и поиска пользователя')
class TestUser:

    @allure.title("Тест успешного создания пользователя")
    def test_create_user(self, super_admin: User, creation_user_data: UserSchema):
        """
        Тест успешного создания пользователя
        :param super_admin: User-сессия с правами SUPER_ADMIN
        :param creation_user_data: Данные для создания пользователя
        """
        with check:
            response = super_admin.api.user_api.create_user(creation_user_data)
        with allure.step('Валидация тела ответа по схеме RegisterUserResponseSchema'):
            with check:
                response_data = RegisterUserResponseSchema.model_validate_json(response.text)
        with allure.step('Проверка id'):
            with check:
                assert response_data.id != '', "ID должен быть не пустым"
        with allure.step('Проверка email'):
            with check:
                assert response_data.email == creation_user_data.email
        with allure.step('Проверка fullName'):
            with check:
                assert response_data.fullName == creation_user_data.fullName
        with allure.step('Проверка roles'):
            with check:
                assert response_data.roles == creation_user_data.roles
        with allure.step('Проверка verified'):
            with check:
                assert response_data.verified
        super_admin.api.user_api.delete_user(response_data.id, expected_status=200)

    @allure.title("Тест получения пользователя по id/email")
    def test_get_user_by_locator(self, super_admin: User, creation_user_data: UserSchema):
        """
        Тест получения пользователя по id/email
        :param super_admin: User-сессия с правами SUPER_ADMIN
        :param creation_user_data: Данные для создания пользователя
        """
        with check:
            created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        with allure.step('Валидация тела ответа по схеме RegisterUserResponseSchema'):
            with check:
                created_user = RegisterUserResponseSchema.model_validate_json(created_user_response.text)
        with check:
            response_by_id = super_admin.api.user_api.get_user(created_user.id)
        with check:
            response_by_email = super_admin.api.user_api.get_user(created_user.email)
        with allure.step('Валидация тела ответа по схеме RegisterUserResponseSchema'):
            with check:
                by_id = RegisterUserResponseSchema.model_validate_json(response_by_id.text)
        with allure.step('Валидация тела ответа по схеме RegisterUserResponseSchema'):
            with check:
                by_email = RegisterUserResponseSchema.model_validate_json(response_by_email.text)
        with allure.step('Проверка ответов by_id и by_email'):
            with check:
                assert by_id == by_email, "Содержание ответов должно быть идентичным"
        with allure.step('Проверка id'):
            with check:
                assert by_id.id != '', "ID должен быть не пустым"
        with allure.step('Проверка email'):
            with check:
                assert by_id.email == creation_user_data.email
        with allure.step('Проверка id'):
            with check:
                assert by_id.fullName == creation_user_data.fullName
        with allure.step('Проверка roles'):
            with check:
                assert by_id.roles == creation_user_data.roles
        with allure.step('Проверка id'):
            with check:
                assert by_id.verified
        super_admin.api.user_api.delete_user(created_user.id, expected_status=200)

    @pytest.mark.slow
    @allure.title("Тест получения пользователя по id с ролью USER")
    def test_get_user_by_id_common_user(self, common_user: User):
        """
        Тест получения пользователя по id с ролью USER
        :param common_user: User-сессия с правами USER
        """
        with check:
            response = common_user.api.user_api.get_user(common_user.email, expected_status=403)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                reponse_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения ответа'):
            with check:
                assert reponse_data.message == FORBIDDEN_MOVIE_ERR_MSG
        with allure.step('Проверка статус-кода'):
            assert reponse_data.statusCode == 403

