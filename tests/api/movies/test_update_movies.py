import pytest
from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager


def test_update_movie(api_manager: ApiManager, movie_data, create_movie_fixture):
    response = api_manager.movie_api.update_movie(create_movie_fixture['id'], movie_data)
    response_data = response.json()
    for key in movie_data:
        assert response_data[key] == movie_data[key],\
            f'Expected {movie_data[key]}, got {response_data[key]} in {key}'
    api_manager.movie_api.delete_movie(response_data['id'])

def test_update_movie_not_found(api_manager: ApiManager, movie_data):
    response = api_manager.movie_api.update_movie(0, movie_data, expected_status=404)
    response_data = response.json()
    assert response_data['message'] == NOT_FOUND_MOVIE_ERR_MSG,\
        f'Expected message: "{NOT_FOUND_MOVIE_ERR_MSG}", got "{response_data['message']}"'