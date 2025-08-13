import allure
import pytest
from constants import NOT_FOUND_MOVIE_ERR_MSG
from schemas.error_schema import BaseError
from schemas.movie_schema import CreateMovieResponseSchema, DeleteMovieResponseSchema, GetMovieResponseSchema, \
    CreateMovieRequestSchema


@allure.title("Тест успешного удаления фильма")
def test_delete_movie(super_admin, create_movie_fixture: CreateMovieResponseSchema):
    find_response = super_admin.api.movie_api.get_movie(create_movie_fixture.id, expected_status=200)
    find_data = GetMovieResponseSchema.model_validate_json(find_response.text)
    delete_response = super_admin.api.movie_api.delete_movie(create_movie_fixture.id, expected_status=200)
    delete_data = DeleteMovieResponseSchema.model_validate_json(delete_response.text)
    find_response_after_delete = super_admin.api.movie_api.get_movie(create_movie_fixture.id, expected_status=404)
    find_response_after_delete_data = BaseError.model_validate_json(find_response_after_delete.text)
    assert find_response_after_delete_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {find_response_after_delete_data.message}'
    assert find_response_after_delete_data.statusCode == 404

@allure.title("Тест успешного удаления нескольких фильмов, id фильма: {fixture_name}")
@pytest.mark.parametrize('fixture_name', ['create_movie_fixture']*5)
def test_delete_movies(super_admin, request, fixture_name):
    fixture_data = request.getfixturevalue(fixture_name)
    movie_id = fixture_data.id
    response = super_admin.api.movie_api.delete_movie(movie_id, expected_status=200)
    response_data = DeleteMovieResponseSchema.model_validate_json(response.text)
    find_response = super_admin.api.movie_api.get_movie(movie_id, expected_status=404)
    find_data = BaseError.model_validate_json(find_response.text)
    assert find_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {find_data.message}'
    assert find_data.statusCode == 404

@allure.title("Тест удаления фильма с несуществующим ID")
def test_delete_movie_not_found(super_admin):
    response = super_admin.api.movie_api.delete_movie(0, expected_status=404)
    response_data = BaseError.model_validate_json(response.text)
    assert response_data.message == NOT_FOUND_MOVIE_ERR_MSG, \
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data.message}'
    assert response_data.statusCode == 404