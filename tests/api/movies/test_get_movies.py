import allure
import pytest
import requests
from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_fixture_shema import MovieFixtureSchema
from schemas.movie_schema import GetMoviesResponseSchema, CreateMovieResponseSchema, GetMovieResponseSchema
from utils.data_generator import DataGenerator as DG


@allure.title("Тест успешного получения списка фильмов")
def test_get_movies(api_manager: ApiManager):
    response = api_manager.movie_api.get_movies()
    response_data = GetMoviesResponseSchema.model_validate_json(response.text)
    assert len(response_data.movies) == 10, f'Expected 10 movies in page, got {len(response_data.movies)}'
    assert len(response_data.movies) == response_data.pageSize,\
        f'Expected {response_data.pageSize} movies in page, got {len(response_data.movies)}'

@allure.title("Тест успешного получения списка фильмов с фильтрами")
def test_get_movies_with_filter(api_manager: ApiManager):
    min_price = 700
    max_price = 1000
    page_size = 5
    response = api_manager.movie_api.get_movies(min_price=min_price,max_price=max_price, page_size=5)
    response_data = GetMoviesResponseSchema.model_validate_json(response.text)
    assert len(response_data.movies) == page_size, f'Expected {page_size} movies in page, got {len(response_data.movies)}'
    assert len(response_data.movies) == response_data.pageSize,\
        f'Expected {response_data.pageSize} movies in page, got {len(response_data.movies)}'
    movies = response_data.movies
    for movie in movies:
        assert min_price <= movie.price <= max_price, 'Price dont match filters'

@allure.title("Тест успешного получения фильма")
def test_get_movie(api_manager: ApiManager, create_and_delete_movie_fixture: MovieFixtureSchema):
    response = api_manager.movie_api.get_movie(create_and_delete_movie_fixture.id)
    response_data = GetMovieResponseSchema.model_validate_json(response.text).model_dump()
    create_and_delete_movie_fixture = create_and_delete_movie_fixture.model_dump()
    # for key in create_and_delete_movie_fixture:
    #     assert response_data[key] == create_and_delete_movie_fixture[key],\
    #         f'Expected {create_and_delete_movie_fixture[key]}, got {response_data[key]} in {key}'

@allure.title("Тест получения несуществующего фильма")
def test_get_movie_not_found(api_manager: ApiManager):
    response = api_manager.movie_api.get_movie(movie_id=0, expected_status=404)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG,\
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data.message}'
    assert response_data.statusCode == 404

@allure.title(
    "Тест получения списка фильмов с параметрами: max_price:{max_price}, min_price:{min_price}, locations:{locations}, genre_id:{genre_id}")
@pytest.mark.slow
@pytest.mark.parametrize(
    "max_price,min_price,locations,genre_id",
    DG.generate_params_for_filters())
def test_get_movies_with_multiply_filters(
        api_manager: ApiManager, max_price: int, min_price: int, locations, genre_id):
    response = api_manager.movie_api.get_movies(
        min_price=min_price, max_price=max_price, locations=locations, genre_id=genre_id)
    response_data = GetMoviesResponseSchema.model_validate_json(response.text)
    for movie in response_data.movies:
        genre_name = requests.get(url=f'https://api.dev-cinescope.coconutqa.ru/genres/{genre_id}').json()['name']
        assert min_price <= movie.price <= max_price, "Out of price"
        assert movie.location == locations, 'Wrong location'
        assert movie.genre.name == genre_name, 'wwrong genre'

