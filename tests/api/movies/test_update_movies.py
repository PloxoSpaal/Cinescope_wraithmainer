import allure
import pytest
from pytest_check import check

from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_schema import CreateMovieRequestSchema, UpdateMovieResponseSchema, CreateMovieResponseSchema
from schemas.user_entity_schema import User


@allure.epic('Функционал фильмов')
@allure.feature('Проверка функциональности обновления фильма')
@pytest.mark.update_movie
class TestUpdateMovie:

    @allure.title("Тест успешного обновления фильма")
    @pytest.mark.slow
    def test_update_movie(
            self, admin: User, movie_data: CreateMovieRequestSchema,
            create_and_delete_movie_fixture: CreateMovieResponseSchema):
        """
        Тест успешного обновления фильма
        :param admin: User-сессия с правами ADMIN
        :param movie_data: Данные для создания фильма
        :param create_and_delete_movie_fixture: Созданный фильм(удаляется после теста)
        """
        with check:
            response = admin.api.movie_api.update_movie(create_and_delete_movie_fixture.id, movie_data)
        movie_data = movie_data.model_dump()
        with allure.step('Валидация тела ответа по схеме UpdateMovieResponseSchema'):
            with check:
                response_data = UpdateMovieResponseSchema.model_validate_json(response.text).model_dump()
        for key in movie_data:
            with allure.step('Проверка значений в ключе {key}'):
                with check:
                    assert response_data[key] == movie_data[key], \
                        f'Expected {movie_data[key]}, got {response_data[key]} in {key}'

    @allure.title("Тест обновления несуществующего фильма")
    def test_update_movie_not_found(self, admin: User, movie_data: CreateMovieRequestSchema):
        """
        Тест обновления несуществующего фильма
        :param admin: User-сессия с правами ADMIN
        :param movie_data: Данные для создания фильма
        """
        with check:
            response = admin.api.movie_api.update_movie(0, movie_data, expected_status=404)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
                f'Expected message: "{NOT_FOUND_MOVIE_ERR_MSG}", got "{response_data.message}"'
