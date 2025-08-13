import allure
import pytest
from utils.data_generator import DataGenerator
from constants import AUTH_ERR_MSG
from schemas.user_fixture_schema import UserSchema, UserFixtureSchema, RegisterUserResponseSchema
from schemas.auth_shema import LoginRequestSchema, LoginResponseSchema


@allure.title("Тест успешной регистрации пользователя")
def test_register_user(test_user: UserSchema, admin):
    """
    Тест на регистрацию пользователя.
    """
    response = admin.api.auth_api.register_user(test_user, expected_status=201)
    response_data = RegisterUserResponseSchema.model_validate_json(response.text)
    assert response_data.email == test_user.email, "Email не совпадает"
    admin.api.user_api.delete_user(response_data.id, expected_status=200)

@allure.title("Тест успешного логина пользователя")
def test_login_user(super_admin, registered_user: UserFixtureSchema):
    """
    Тест на авторизацию пользователя.
    """
    login_data = LoginRequestSchema(email=registered_user.email, password=registered_user.password)
    response = super_admin.api.auth_api.login_user(login_data, expected_status=200)
    response_data = LoginResponseSchema.model_validate_json(response.text)
    assert response_data.email == registered_user.email, "Email не совпадает"
    super_admin.api.user_api.delete_user(response_data.id, expected_status=200)

@allure.title("Тест логина пользователя с неверным паролем")
def test_login_user_with_incorrect_password(admin, registered_user: UserFixtureSchema):
    login_data = LoginRequestSchema(email=registered_user.email, password=DataGenerator.generate_random_password())
    response = admin.api.auth_api.login_user(login_data, expected_status=401)
    response_data = response.json()
    assert response_data['message'] == AUTH_ERR_MSG, \
        f'Expected error message: "{AUTH_ERR_MSG}", got "{response_data['message']}"'
    admin.api.user_api.delete_user(registered_user.id, expected_status=200)