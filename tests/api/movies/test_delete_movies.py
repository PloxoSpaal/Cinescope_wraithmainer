import allure
import pytest
from pytest_check import check

from constants import NOT_FOUND_MOVIE_ERR_MSG
from schemas.error_schema import BaseError
from schemas.movie_schema import CreateMovieResponseSchema, DeleteMovieResponseSchema, GetMovieResponseSchema, \
    CreateMovieRequestSchema
from schemas.user_entity_schema import User


@allure.epic('Функционал фильмов')
@allure.feature('Проверка функциональности удаления фильмов')
@pytest.mark.delete_movie
class TestDeleteMovie:

    @allure.title("Тест успешного удаления фильма")
    def test_delete_movie(self, super_admin: User, create_movie_fixture: CreateMovieResponseSchema):
        """
        Тест успешного удаления фильма
        :param super_admin: User-сессия с правами SUPER_ADMIN
        :param create_movie_fixture: Созданный экземпляр фильма
        """
        with check:
            find_response = super_admin.api.movie_api.get_movie(create_movie_fixture.id, expected_status=200)
        with allure.step('Валидация тела ответа по схеме GetMovieResponseSchema'):
            with check:
                find_data = GetMovieResponseSchema.model_validate_json(find_response.text)
        with check:
            delete_response = super_admin.api.movie_api.delete_movie(create_movie_fixture.id, expected_status=200)
        with allure.step('Валидация тела ответа по схеме DeleteMovieResponseSchema'):
            with check:
                delete_data = DeleteMovieResponseSchema.model_validate_json(delete_response.text)
        with check:
            find_response_after_delete = super_admin.api.movie_api.get_movie(
                create_movie_fixture.id, expected_status=404)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                find_response_after_delete_data = BaseError.model_validate_json(find_response_after_delete.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert find_response_after_delete_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
                    f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {find_response_after_delete_data.message}'
        with allure.step('Проверка статус-кода'):
            assert find_response_after_delete_data.statusCode == 404

    @allure.title("Тест успешного удаления нескольких фильмов, id фильма: {fixture_name}")
    @pytest.mark.parametrize('fixture_name', ['create_movie_fixture'] * 5)
    def test_delete_movies(self, super_admin: User, request, fixture_name):
        """
        Тест успешного удаления нескольких фильмов
        :param super_admin: User-сессия с правами SUPER_ADMIN
        """
        with check:
            fixture_data = request.getfixturevalue(fixture_name)
        movie_id = fixture_data.id
        with check:
            response = super_admin.api.movie_api.delete_movie(movie_id, expected_status=200)
        with allure.step('Валидация тела ответа по схеме DeleteMovieResponseSchema'):
            with check:
                response_data = DeleteMovieResponseSchema.model_validate_json(response.text)
        with check:
            find_response = super_admin.api.movie_api.get_movie(movie_id, expected_status=404)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                find_data = BaseError.model_validate_json(find_response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert find_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
                    f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {find_data.message}'
        with allure.step('Проверка статус-кода'):
            assert find_data.statusCode == 404

    @allure.title("Тест удаления фильма с несуществующим ID")
    def test_delete_movie_not_found(self, super_admin: User):
        """
        Тест удаления фильма с несуществующим ID
        :param super_admin: User-сессия с правами SUPER_ADMIN
        """
        with check:
            response = super_admin.api.movie_api.delete_movie(0, expected_status=404)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
                    f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data.message}'
        with allure.step('Проверка статус-кода'):
            assert response_data.statusCode == 404
