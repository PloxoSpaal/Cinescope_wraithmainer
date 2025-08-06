import random
import pytest
import faker
import requests
from constants import BASE_URL, PASSWORD, USERNAME, HEADERS, AUTH_BASE_URL, OK_STATUS_CODE, REGISTER_ENDPOINT, LOGIN_ENDPOINT, USER_CREDS
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager

fake = faker.Faker()

@pytest.fixture(scope='session')
def genre_id():
    response = requests.get(f'{BASE_URL}/genres')
    result = list(map(lambda x: x['id'], response.json()))
    return result

@pytest.fixture
def movie_data(genre_id):
    data = {
        "name": fake.sentence(),
        "imageUrl": "https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
        "price": fake.random_int(99, 1000),
        "description": fake.text(),
        "location": random.choice(['MSK', 'SPB']),
        "published": fake.boolean(65),
        "genreId": random.choice(genre_id)
    }
    return data

@pytest.fixture
def incorrect_movie_data(genre_id):
    data = {
        "name": fake.sentence(),
        "imageUrl": "https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
        "price": fake.random_int(99, 1000),
        "description": fake.text(),
        "location": fake.random_int(),
        "published": fake.sentence(),
        "genreId": random.choice(genre_id)
    }
    return data

@pytest.fixture(scope='session')
def admin_auth_session():
    data = {
        "email": USERNAME,
        "password": PASSWORD
    }
    session = requests.Session()
    session.headers.update(HEADERS)
    response = requests.post(
        f'{AUTH_BASE_URL}/login',
        headers=HEADERS,
        json=data
    )
    assert response.status_code in OK_STATUS_CODE, 'Auth Error'
    access_token = response.json().get('accessToken')
    assert access_token is not None, 'Access Token is not defined'
    refresh_token = response.json().get('accessToken')
    assert refresh_token is not None, 'Refresh Token is not defined'
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "X-Refresh-Token": refresh_token
    })
    return session

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def auth_session(test_user):
    # Регистрируем нового пользователя
    register_url = f"{AUTH_BASE_URL}/register"
    response = requests.post(register_url, json=test_user, headers=HEADERS)
    assert response.status_code == 201, "Ошибка регистрации пользователя"
    login_url = f"{AUTH_BASE_URL}/login"
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }
    response = requests.post(login_url, json=login_data, headers=HEADERS)
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("accessToken")
    assert token is not None, "Токен доступа отсутствует в ответе"
    session = requests.Session()
    session.headers.update(HEADERS)
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session

@pytest.fixture(scope="session")
def auth_requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_BASE_URL)

@pytest.fixture(scope="session")
def cinescope_requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def admin_cinescope_requester(admin_auth_session):
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=admin_auth_session, base_url=BASE_URL)

@pytest.fixture(scope="function")
def registered_user(auth_requester, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture
def create_movie_fixture(movie_data, api_manager):
    """
    Фикстура для создания фильма.
    """
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.create_movie(
        movie_data=movie_data,
        expected_status=201
    )
    response_data = response.json()
    return response_data


