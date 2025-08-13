import pytest
import allure
from assertions.db_assertions import assert_movie_in_db, assert_movie_values_in_db
from constants import USER_CREDS, UNATHORIZED_MOVIE_ERR_MSG, BAD_REQ_MOVIE_ERR_MSG, SAME_NAME_MOVIE_ERR_MSG, \
    FORBIDDEN_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_fixture_shema import MovieFixtureSchema
from schemas.movie_schema import CreateMovieRequestSchema, CreateMovieResponseSchema, GetMovieResponseSchema


@pytest.mark.slow
@allure.title("Тест успешного создания пользователя")
def test_create_movie(movie_data: CreateMovieRequestSchema, admin, db_session):
    response = admin.api.movie_api.create_movie(movie_data, expected_status=201)
    movie_fixture = MovieFixtureSchema(
        request=movie_data,
        response=CreateMovieResponseSchema.model_validate_json(response.text))
    assert_movie_in_db(db_session, movie_fixture.id)
    assert_movie_values_in_db(db_session, movie_fixture)
    movie_data =movie_data.model_dump()
    response_data = CreateMovieResponseSchema.model_validate_json(response.text).model_dump()
    for key in movie_data:
        assert response_data[key] == movie_data[key], f'Expected {movie_data[key]}, got {response_data[key]}'
    response_get = admin.api.movie_api.get_movie(response_data['id'], expected_status=200)
    get_movie = GetMovieResponseSchema.model_validate_json(response_get.text).model_dump()
    for key in response_data:
        assert get_movie[key] == response_data[key], \
            f'Expected {response_data[key]}, got {get_movie[key]}'
    admin.api.movie_api.delete_movie(response_data['id'])

@allure.title("Тест создания филмьа с некорректными данными")
def test_create_movie_with_incorrect_movie_data(super_admin, incorrect_movie_data: CreateMovieRequestSchema):
    response = super_admin.api.movie_api.create_movie(incorrect_movie_data, expected_status=400)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == 'Некорректные данные', \
        f'Expected error: "Некорректные данные", got "{response_data.message}"'
    assert response_data.statusCode == 400

@allure.title("Тест создания фильма с уже используемым именем")
def test_create_movie_with_same_name(admin, movie_data: CreateMovieRequestSchema):
    response = admin.api.movie_api.create_movie(movie_data)
    response_data = CreateMovieResponseSchema.model_validate_json(response.text)
    response_error = admin.api.movie_api.create_movie(movie_data, expected_status=409)
    response_data_error = BaseError.model_validate_json(response_error.text)
    assert response_data_error.message == SAME_NAME_MOVIE_ERR_MSG, \
        f'Expected error: "{SAME_NAME_MOVIE_ERR_MSG}", got "{response_data_error.message}"'
    assert response_data_error.statusCode == 409
    admin.api.movie_api.delete_movie(response_data.id)

@allure.title("Тест создания фильма без авторизации")
def test_create_movie_unathorized(api_manager: ApiManager, movie_data: CreateMovieRequestSchema):
    response = api_manager.movie_api.create_movie(movie_data=movie_data, expected_status=401)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == UNATHORIZED_MOVIE_ERR_MSG, \
        f'Expected error message: "{UNATHORIZED_MOVIE_ERR_MSG}", got "{response_data.message}"'


@pytest.mark.slow
@allure.title("Тест создания фильма с ролью USER")
def test_create_movie_user_role(movie_data: CreateMovieRequestSchema, common_user):
    response = common_user.api.movie_api.create_movie(movie_data, expected_status=403)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == FORBIDDEN_MOVIE_ERR_MSG, \
        f'Expected error message: "{FORBIDDEN_MOVIE_ERR_MSG}", got "{response_data.message}"'
