import pytest
import allure
from constants import FORBIDDEN_MOVIE_ERR_MSG
from schemas.error_schema import BaseError
from schemas.user_fixture_schema import UserSchema, RegisterUserResponseSchema
from schemas.user_schema import CreateUserRequestSchema


class TestUser:

    @allure.title("Тест успешного создания пользователя")
    def test_create_user(self, super_admin, creation_user_data: UserSchema):
        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = RegisterUserResponseSchema.model_validate_json(response.text)
        assert response_data.id != '', "ID должен быть не пустым"
        assert response_data.email == creation_user_data.email
        assert response_data.fullName == creation_user_data.fullName
        assert response_data.roles == creation_user_data.roles
        assert response_data.verified
        super_admin.api.user_api.delete_user(response_data.id, expected_status=200)

    @allure.title("Тест получения пользователя по id/email")
    def test_get_user_by_locator(self, super_admin, creation_user_data: UserSchema):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponseSchema.model_validate_json(created_user_response.text)
        response_by_id = super_admin.api.user_api.get_user(created_user.id)
        response_by_email = super_admin.api.user_api.get_user(created_user.email)
        by_id = RegisterUserResponseSchema.model_validate_json(response_by_id.text)
        by_email = RegisterUserResponseSchema.model_validate_json(response_by_email.text)
        assert by_id == by_email, "Содержание ответов должно быть идентичным"
        assert by_id.id != '', "ID должен быть не пустым"
        assert by_id.email == creation_user_data.email
        assert by_id.fullName == creation_user_data.fullName
        assert by_id.roles == creation_user_data.roles
        assert by_id.verified
        super_admin.api.user_api.delete_user(created_user.id, expected_status=200)

    @pytest.mark.slow
    @allure.title("Тест получения пользователя по id с ролью USER")
    def test_get_user_by_id_common_user(self, common_user):
        response = common_user.api.user_api.get_user(common_user.email, expected_status=403)
        reponse_data = BaseError.model_validate_json(response.text)
        assert reponse_data.message == FORBIDDEN_MOVIE_ERR_MSG
        assert reponse_data.statusCode == 403

