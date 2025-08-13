import allure
import pytest
from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager
from schemas.error_schema import BaseError
from schemas.movie_schema import CreateMovieRequestSchema, UpdateMovieResponseSchema, CreateMovieResponseSchema

@allure.title("Тест успешного обновления фильма")
@pytest.mark.slow
def test_update_movie(
        admin, movie_data: CreateMovieRequestSchema, create_and_delete_movie_fixture: CreateMovieResponseSchema):
    response = admin.api.movie_api.update_movie(create_and_delete_movie_fixture.id, movie_data)
    movie_data = movie_data.model_dump()
    response_data = UpdateMovieResponseSchema.model_validate_json(response.text).model_dump()
    for key in movie_data:
        assert response_data[key] == movie_data[key],\
            f'Expected {movie_data[key]}, got {response_data[key]} in {key}'

@allure.title("Тест обновления несуществующего фильма")
def test_update_movie_not_found(admin, movie_data: CreateMovieRequestSchema):
    response = admin.api.movie_api.update_movie(0, movie_data, expected_status=404)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG,\
        f'Expected message: "{NOT_FOUND_MOVIE_ERR_MSG}", got "{response_data.message}"'