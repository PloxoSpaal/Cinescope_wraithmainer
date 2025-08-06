import pytest
from constants import NOT_FOUND_MOVIE_ERR_MSG, USER_CREDS
from api.api_manager import ApiManager


def test_delete_movie(api_manager: ApiManager, create_movie_fixture):
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.delete_movie(create_movie_fixture['id'])
    find_response = api_manager.movie_api.get_movie(create_movie_fixture['id'], expected_status=404)
    assert find_response.json()['message'] == NOT_FOUND_MOVIE_ERR_MSG, \
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data["message"]}'

def test_delete_movie_not_found(api_manager: ApiManager):
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.delete_movie(0, expected_status=404)
    response_data = response.json()
    assert response_data['message'] == NOT_FOUND_MOVIE_ERR_MSG, \
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data["message"]}'