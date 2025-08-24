import allure
import pytest
import requests
from pytest_check import check

from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_fixture_shema import MovieFixtureSchema
from schemas.movie_schema import GetMoviesResponseSchema, CreateMovieResponseSchema, GetMovieResponseSchema
from utils.data_generator import DataGenerator as DG


@allure.epic('Функционал фильмов')
@allure.feature('Проверка функциональности получения информации о фильме')
@pytest.mark.get_movie
class TestGetMovie:

    @allure.title("Тест успешного получения списка фильмов")
    def test_get_movies(self, api_manager: ApiManager):
        """
        Тест успешного получения списка фильмов
        :param api_manager: Экземпляр ApiManager
        """
        response = api_manager.movie_api.get_movies()
        response_data = GetMoviesResponseSchema.model_validate_json(response.text)
        with check:
            assert len(response_data.movies) == 10, f'Expected 10 movies in page, got {len(response_data.movies)}'
        with check:
            assert len(response_data.movies) == response_data.pageSize, \
                f'Expected {response_data.pageSize} movies in page, got {len(response_data.movies)}'

    @allure.title("Тест успешного получения списка фильмов с фильтрами")
    def test_get_movies_with_filter(self, api_manager: ApiManager):
        """
        Тест успешного получения списка фильмов с фильтрами
        :param api_manager: Экземпляр ApiManager
        """
        min_price = 700
        max_price = 1000
        page_size = 5
        with check:
            response = api_manager.movie_api.get_movies(min_price=min_price, max_price=max_price, page_size=5)
        with allure.step('Валидация тела ответа по схеме GetMoviesResponseSchema'):
            with check:
                response_data = GetMoviesResponseSchema.model_validate_json(response.text)
        with allure.step('Проверка количества фильмов в списке'):
            with check:
                assert len(
                    response_data.movies) == page_size, f'Expected {page_size} movies in page, got {len(response_data.movies)}'
        with allure.step('Проверка количества фильмов в pageSize'):
            with check:
                assert len(response_data.movies) == response_data.pageSize, \
                    f'Expected {response_data.pageSize} movies in page, got {len(response_data.movies)}'
        movies = response_data.movies
        for movie in movies:
            with allure.step('Проверка стоимости фильма'):
                with check:
                    assert min_price <= movie.price <= max_price, 'Price dont match filters'

    @allure.title("Тест успешного получения фильма")
    def test_get_movie(self, api_manager: ApiManager, create_and_delete_movie_fixture: MovieFixtureSchema):
        """
        Тест успешного получения фильма
        :param api_manager: Экземпляр ApiManager
        :param create_and_delete_movie_fixture: Созданный фильм(удаляется после теста)
        """
        with check:
            response = api_manager.movie_api.get_movie(create_and_delete_movie_fixture.id)
        with allure.step('Валидация тела ответа по схеме GetMovieResponseSchema'):
            with check:
                response_data = GetMovieResponseSchema.model_validate_json(response.text).model_dump()
        create_and_delete_movie_fixture = create_and_delete_movie_fixture.model_dump()

    @allure.title("Тест получения несуществующего фильма")
    def test_get_movie_not_found(self, api_manager: ApiManager):
        """
        Тест получения несуществующего фильма
        :param api_manager: Экземпляр ApiManager
        """
        with check:
            response = api_manager.movie_api.get_movie(movie_id=0, expected_status=404)
        with allure.step('Валидация тела ответа по схеме BaseError'):
            with check:
                response_data = BaseError.model_validate_json(response.text)
        with allure.step('Проверка сообщения в теле ответа'):
            with check:
                assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
                    f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data.message}'
        with allure.step('Проверка статус-кода'):
            assert response_data.statusCode == 404

    @allure.title(
        "Тест получения списка фильмов с параметрами:"
        " max_price: {max_price}, min_price: {min_price}, locations: {locations}, genre_id: {genre_id}")
    @pytest.mark.slow
    @pytest.mark.parametrize(
        "max_price,min_price,locations,genre_id",
        DG.generate_params_for_filters())
    def test_get_movies_with_multiply_filters(
            self, api_manager: ApiManager, max_price: int, min_price: int, locations: list, genre_id: str):
        """
        Тест получения списка фильмов с параметрами
        :param api_manager: Экземпляр ApiManager
        :param max_price: Максимальная стоимость фильма
        :param min_price: Минимальная стоимость фильма
        :param locations: Список локаций
        :param genre_id: id жанра фильма
        """
        with check:
            response = api_manager.movie_api.get_movies(
                min_price=min_price, max_price=max_price, locations=locations, genre_id=genre_id)
        with allure.step('Валидация тела ответа по схеме GetMoviesResponseSchema'):
            with check:
                response_data = GetMoviesResponseSchema.model_validate_json(response.text)
        for movie in response_data.movies:
            with allure.step('Проверка данных в фильме'):
                with check:
                    genre_name = requests.get(url=f'https://api.dev-cinescope.coconutqa.ru/genres/{genre_id}').json()['name']
                with allure.step('Проверка цены фильма'):
                    with check:
                        assert min_price <= movie.price <= max_price, "Out of price"
                with allure.step('Проверка локации фильма'):
                    with check:
                        assert movie.location == locations, 'Wrong location'
                with allure.step('Проверка жанра фильма'):
                    assert movie.genre.name == genre_name, 'Wrong genre'
