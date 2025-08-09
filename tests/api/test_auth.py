import pytest
from constants import USER_CREDS
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from constants import AUTH_ERR_MSG


def test_register_user(test_user, api_manager: ApiManager):
    """
    Тест на регистрацию пользователя.
    """
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.auth_api.register_user(test_user, expected_status=201)
    response_data = response.json()
    assert response_data["email"] == test_user["email"], "Email не совпадает"
    assert "id" in response_data, "ID пользователя отсутствует в ответе"
    assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
    assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"
    api_manager.user_api.delete_user(response_data['id'], expected_status=200)

def test_register_and_login_user(api_manager: ApiManager, registered_user):
    """
    Тест на регистрацию и авторизацию пользователя.
    """
    api_manager.auth_api.authenticate(USER_CREDS)
    login_data = {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }
    response = api_manager.auth_api.login_user(login_data, expected_status=200)
    response_data = response.json()
    assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
    assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
    api_manager.user_api.delete_user(registered_user['id'], expected_status=200)

def test_authenticate_user_with_incorrect_password(api_manager: ApiManager, registered_user):
    api_manager.auth_api.authenticate(USER_CREDS)
    login_data = {
        "email": registered_user["email"],
        "password": DataGenerator.generate_random_password()
    }
    response = api_manager.auth_api.login_user(login_data, expected_status=401)
    response_data = response.json()
    assert response_data['message'] == AUTH_ERR_MSG, \
        f'Expected error message: "{AUTH_ERR_MSG}", got "{response_data['message']}"'
    api_manager.user_api.delete_user(registered_user['id'], expected_status=200)