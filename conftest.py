import os
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, Page
import pytest
import faker
import requests
import allure
import os
from constants import BASE_URL, HEADERS, AUTH_BASE_URL, OK_STATUS_CODE, REGISTER_ENDPOINT, Roles
from schemas.auth_shema import LoginRequestSchema
from schemas.db_schema.user_db_schema import UserTableDBSchema
from schemas.movie_fixture_shema import MovieFixtureSchema
from schemas.movie_schema import CreateMovieRequestSchema, CreateMovieResponseSchema
from ui.login_page import LoginPage
from ui.main_page import MainPage
from ui.register_page import RegisterPage
from utils.data_generator import DataGenerator
from schemas.user_entity_schema import User
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from typing import List
from dotenv import load_dotenv
from schemas.user_fixture_schema import UserSchema, RegisterUserResponseSchema, UserFixtureSchema
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, text

fake = faker.Faker()
load_dotenv()
DEFAULT_UI_TIMEOUT = 10000


@allure.step('Создание экземпляра браузера')
@pytest.fixture(scope="session")
def browser(playwright):
    """
    Фикстура создаёт объект браузера для UI-тестов
    :param playwright: фикстура playwright
    """
    browser = playwright.chromium.launch(headless=False, args=['--start-maximized'])
    yield browser
    browser.close()


@allure.step('Создание экземпляра Context')
@pytest.fixture(scope="function")
def context(browser):
    """
    Фикстура создаёт экземпляр Context для UI-тестов
    :param browser: Экземпляр браузера
    """
    context = browser.new_context(no_viewport=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    context.close()


@allure.step('Создание экземпляра страницы')
@pytest.fixture(scope="function")
def page(context) -> Page:
    """
    Фикстура создаёт экземпляр Page для UI-тестов
    :param context: Экземпляр Context
    """
    page = context.new_page()
    yield page
    page.close()


@allure.step('Создание экземпляра страницы регистрации')
@pytest.fixture(scope='function')
def register_page(page) -> RegisterPage:
    """
    Фикстура создаёт экземпляр страницы регистрации для UI-тестов
    :param page: Экземпляр Page
    """
    return RegisterPage(page)


@allure.step('Создание экземпляра страницы логина')
@pytest.fixture(scope='function')
def login_page(page) -> LoginPage:
    """
    Фикстура создаёт экземпляр страницы логина для UI-тестов
    :param page: Экземпляр Page
    """
    return LoginPage(page)


@allure.step('Создание экземпляра главной страницы')
@pytest.fixture(scope='function')
def main_page(page) -> MainPage:
    """
    Фикстура создаёт экземпляр главной страницы для UI-тестов
    :param page: Экземпляр Page
    """
    return MainPage(page)


@allure.step('Получение id всех жанров фильмов')
@pytest.fixture(scope='session')
def genre_id() -> List[int]:
    """
    Фикстура получения всех ID жанров
    :return: Список ID жанров
    """
    response = requests.get(f'{BASE_URL}/genres')
    result = list(map(lambda x: x['id'], response.json()))
    return result


@allure.step('Подготовка данных для создания фильма')
@pytest.fixture
def movie_data(genre_id) -> CreateMovieRequestSchema:
    """
    Фикетура создаёт данные для создания фильма
    :param genre_id: Список ID жанров
    :return:
    """
    return CreateMovieRequestSchema(
        name=DataGenerator.generate_random_movie_name(),
        imageUrl="https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
        price=DataGenerator.generate_random_int(99, 1000),
        description=DataGenerator.generate_random_text(),
        location=DataGenerator.generate_random_choice(['MSK', 'SPB']),
        published=DataGenerator.generate_random_bool(),
        genreId=DataGenerator.generate_random_choice(genre_id))


@allure.step('Подготовка некорректных данных для создания фильма')
@pytest.fixture
def incorrect_movie_data(genre_id) -> CreateMovieRequestSchema:
    """
    Фикетура создаёт некорректные данные для создания фильма
    :param genre_id: Список ID жанров
    """
    return CreateMovieRequestSchema(
        name=DataGenerator.generate_random_movie_name(),
        imageUrl="https://poknok.art/uploads/posts/2022-11/thumbs/1668713844_33-poknok-art-p-ptitsi-belom-fone-foto-35.png",
        price=DataGenerator.generate_random_int(99, 1000),
        description=DataGenerator.generate_random_text(),
        location=DataGenerator.generate_random_choice(['MSK', 'SPB']),
        published=DataGenerator.generate_random_bool(),
        genreId=111111111)


@allure.step('Подготовка данных для создания пользователя')
@pytest.fixture(scope="function")
def test_user() -> UserSchema:
    """
    Фикстура создаёт случайного пользователя для тестов
    """
    random_password = DataGenerator.generate_random_password()
    return UserSchema(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER])


@allure.step('Создание CustomRequester, связанного с управленеим пользователями')
@pytest.fixture(scope="session")
def auth_requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=AUTH_BASE_URL)


@allure.step('Создание CustomRequester, связанного с управленеим фильмами')
@pytest.fixture(scope="session")
def cinescope_requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@allure.step('Регистрация пользователя с ответом UserFixtureSchema')
@pytest.fixture(scope="function")
def registered_user(auth_requester, test_user: UserSchema) -> UserFixtureSchema:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = auth_requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user.model_dump(),
        expected_status=201
    )
    return UserFixtureSchema(
        request=test_user,
        response=RegisterUserResponseSchema.model_validate_json(response.text))


@allure.step('Создание http-сессии')
@pytest.fixture(scope="session")
def session() -> Session:
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@allure.step('Создание экземпляра ApiManager')
@pytest.fixture(scope="session")
def api_manager(session) -> ApiManager:
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)


@allure.step('Создание фильма, удаление фильма после теста')
@pytest.fixture
def create_and_delete_movie_fixture(
        movie_data: CreateMovieRequestSchema, super_admin) -> MovieFixtureSchema:
    """
    Фикстура для создания фильма.
    """
    response = super_admin.api.movie_api.create_movie(
        movie_data=movie_data,
        expected_status=201
    )
    response_data = CreateMovieResponseSchema.model_validate_json(response.text)
    movie_fixture = MovieFixtureSchema(request=movie_data, response=response_data)
    yield movie_fixture
    super_admin.api.movie_api.delete_movie(movie_fixture.id)


@allure.step('Создание фильма')
@pytest.fixture
def create_movie_fixture(movie_data: CreateMovieRequestSchema, super_admin) -> MovieFixtureSchema:
    """
    Фикстура для создания фильма.
    """
    response = super_admin.api.movie_api.create_movie(
        movie_data=movie_data,
        expected_status=201
    )
    response_data = CreateMovieResponseSchema.model_validate_json(response.text)
    movie_fixture = MovieFixtureSchema(request=movie_data, response=response_data)
    return movie_fixture


@allure.step('Создание http-сессии пользователя')
@pytest.fixture
def user_session():
    """
    Фикстура для создания пула сессий пользователей
    :return:
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@allure.step('Создание http-сессии с ролью SUPER_ADMIN')
@pytest.fixture
def super_admin(user_session) -> User:
    """
    Фикстура для создания сессии с ролью SUPER_ADMIN
    :param user_session:
    """
    new_session = user_session()

    super_admin = User(
        email=os.getenv('SUPER_ADMIN_USERNAME'),
        password=os.getenv('SUPER_ADMIN_PASSWORD'),
        roles=[Roles.SUPER_ADMIN],
        api=new_session)
    creds = LoginRequestSchema(email=super_admin.email, password=super_admin.password)

    super_admin.api.auth_api.authenticate(creds)
    return super_admin


@allure.step('Создание пользовательских данных')
@pytest.fixture(scope="function")
def creation_user_data(test_user: UserSchema) -> UserSchema:
    """
    Фикстура для создания пользовательских данных
    :param test_user:
    :return:
    """
    return UserSchema(
        email=test_user.email,
        fullName=test_user.fullName,
        password=test_user.password,
        passwordRepeat=test_user.passwordRepeat,
        roles=test_user.roles,
        verified=True,
        banned=False)


@allure.step('Создание http-сессии с ролью USER')
@pytest.fixture
def common_user(user_session, super_admin, creation_user_data: UserSchema) -> User:
    """
    Фикстура для создания сессии с ролью USER
    :param user_session:
    :param super_admin:
    :param creation_user_data:
    """
    new_session = user_session()

    common_user = User(
        email=creation_user_data.email,
        password=creation_user_data.password,
        roles=[Roles.USER],
        api=new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    creds = LoginRequestSchema(email=common_user.email, password=common_user.password)
    common_user.api.auth_api.authenticate(creds)
    return common_user


@allure.step('Создание http-сессии с ролью ADMIN')
@pytest.fixture
def admin(user_session) -> User:
    """
    Фикстура для создания сессии с ролью ADMIN
    :param user_session:
    :return:
    """
    new_session = user_session()

    admin = User(
        email=os.getenv('SUPER_ADMIN_USERNAME'),
        password=os.getenv('SUPER_ADMIN_PASSWORD'),
        roles=[Roles.ADMIN],
        api=new_session)

    creds = LoginRequestSchema(email=admin.email, password=admin.password)
    admin.api.auth_api.authenticate(creds)
    return admin


@allure.step('Создание engine для запросов в БД')
@pytest.fixture
def db_engine() -> create_engine:
    """
    Фикстура для создания экземпляра create_engine для запросов в БД
    """
    connection_string = \
        (f"postgresql+psycopg2://"
         f"{os.getenv('DB_USERNAME')}:"
         f"{os.getenv('DB_PASSWORD')}@"
         f"{os.getenv('DB_HOST')}:"
         f"{os.getenv('DB_PORT')}/"
         f"{os.getenv('DB_NAME')}")
    engine = create_engine(connection_string)
    return engine


@allure.step('Создание DB-сессии для запросов в БД')
@pytest.fixture
def db_session(db_engine) -> Session:
    """
    Фикстура для создания экземпляра Session для запросов в БД
    """
    session = Session(db_engine)
    yield session
    session.close()


@allure.step('Создание пользователя в БД')
@pytest.fixture
def db_create_user(db_session, test_user):
    """
    Фикстура для добавления пользовтеля в БД
    :param db_session: Сессия для запросов в БД
    :param test_user: Данные пользователя
    """
    user = UserTableDBSchema(
        id=DataGenerator.generate_random_uuid(),
        email=test_user.email,
        full_name=test_user.fullName,
        password=test_user.password,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        verified=False,
        banned=False,
        roles='{USER}'
    )
    db_session.add(user)
    db_session.commit()
    yield db_session
    db_session.delete(user)
    db_session.commit()
    db_session.close()
