import pytest
import allure
from pytest_check import check
from sqlalchemy.orm import Session

from assertions.db_assertions import assert_movie_in_db, assert_movie_values_in_db
from constants import USER_CREDS, UNATHORIZED_MOVIE_ERR_MSG, BAD_REQ_MOVIE_ERR_MSG, SAME_NAME_MOVIE_ERR_MSG, \
    FORBIDDEN_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_fixture_shema import MovieFixtureSchema
from schemas.movie_schema import CreateMovieRequestSchema, CreateMovieResponseSchema, GetMovieResponseSchema
from schemas.user_entity_schema import User


@allure.epic('Функционал фильмов')
@allure.feature('Проверка функциональности создания фильмов')
@pytest.mark.create_movie
class TestCreateMovie:

    @pytest.mark.slow
    @allure.title("Тест успешного создания фильма")
    def test_create_movie(self, movie_data: CreateMovieRequestSchema, admin: User, db_session: Session):
        """
        Тест успешного создания фильма
        :param movie_data: Данные для создания фильма
        :param admin: User-сессия с правами ADMIN
        :param db_session: Сессия для работы с БД
        """
        with check:
            response = admin.api.movie_api.create_movie(movie_data, expected_status=201)
        with allure.step('Создание экземпляра MovieFixtureSchema'):
            with check:
                movie_fixture = MovieFixtureSchema(
                    request=movie_data,
                    response=CreateMovieResponseSchema.model_validate_json(response.text))
        with check:
            assert_movie_in_db(db_session, movie_fixture.id)
        with check:
            assert_movie_values_in_db(db_session, movie_fixture)
        movie_data = movie_data.model_dump()
        with allure.step('Валидация тела ответа по схеме CreateMovieResponseSchema'):
            with check:
                response_data = CreateMovieResponseSchema.model_validate_json(response.text).model_dump()
        for key in movie_data:
            with allure.step('Проверка значений в ключе {key}'):
                with check:
                    assert response_data[key] == movie_data[key], f'Expected {movie_data[key]}, got {response_data[key]}'
        with check:
            response_get = admin.api.movie_api.get_movie(response_data['id'], expected_status=200)
        with allure.step('Валидация тела ответа по схеме GetMovieResponseSchema'):
            with check:
                get_movie = GetMovieResponseSchema.model_validate_json(response_get.text).model_dump()
        for key in response_data:
            with allure.step('Проверка значений в ключе {key}'):
                with check:
                    assert get_movie[key] == response_data[key], \
                f'Expected {response_data[key]}, got {get_movie[key]}'
        admin.api.movie_api.delete_movie(response_data['id'])

    @allure.title("Тест создания фильма с некорректными данными")
    def test_create_movie_with_incorrect_movie_data(
            self, super_admin: User, incorrect_movie_data: CreateMovieRequestSchema):
        """
        Тест создания фильма с некорректными данными
        :param super_admin: User-сессия с правами SUPER_ADMIN
        :param incorrect_movie_data: Некорректные данные для создания фильма
        """
        with check:
            response = super_admin.api.movie_api.create_movie(incorrect_movie_data, expected_status=400)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert response_data.message == 'Некорректные данные', \
                    f'Expected error: "Некорректные данные", got "{response_data.message}"'
        assert response_data.statusCode == 400

    @allure.title("Тест создания фильма с уже используемым именем")
    def test_create_movie_with_same_name(self, admin: User, movie_data: CreateMovieRequestSchema):
        """
        Тест создания фильма с уже используемым именем
        :param admin: User-сессия с правами ADMIN
        :param movie_data: Данные для создания фильма
        """
        with check:
            response = admin.api.movie_api.create_movie(movie_data)
        with allure.step('Валидация тела ответа по схеме CreateMovieResponseSchema'):
            with check:
                response_data = CreateMovieResponseSchema.model_validate_json(response.text)
        with check:
            response_error = admin.api.movie_api.create_movie(movie_data, expected_status=409)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data_error = BaseError.model_validate_json(response_error.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert response_data_error.message == SAME_NAME_MOVIE_ERR_MSG, \
                    f'Expected error: "{SAME_NAME_MOVIE_ERR_MSG}", got "{response_data_error.message}"'
        with allure.step('Проверка статус-кода'):
            with check:
                assert response_data_error.statusCode == 409
        admin.api.movie_api.delete_movie(response_data.id)

    @allure.title("Тест создания фильма без авторизации")
    def test_create_movie_unathorized(self, api_manager: ApiManager, movie_data: CreateMovieRequestSchema):
        """
        Тест создания фильма без авторизации
        :param api_manager: Экземпляр ApiManager
        :param movie_data: Данные для создания фильма
        """
        with check:
            response = api_manager.movie_api.create_movie(movie_data=movie_data, expected_status=401)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            assert response_data.message == UNATHORIZED_MOVIE_ERR_MSG, \
                f'Expected error message: "{UNATHORIZED_MOVIE_ERR_MSG}", got "{response_data.message}"'

    @pytest.mark.slow
    @allure.title("Тест создания фильма с ролью USER")
    def test_create_movie_user_role(self, movie_data: CreateMovieRequestSchema, common_user: User):
        """
        Тест создания фильма с ролью USER
        :param movie_data: Данные для создания фильма
        :param common_user: User-сессия с правами USER
        """
        with check:
            response = common_user.api.movie_api.create_movie(movie_data, expected_status=403)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            assert response_data.message == FORBIDDEN_MOVIE_ERR_MSG, \
                f'Expected error message: "{FORBIDDEN_MOVIE_ERR_MSG}", got "{response_data.message}"'
