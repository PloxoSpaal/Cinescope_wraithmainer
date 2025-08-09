import pytest
from constants import USER_CREDS, UNATHORIZE_MOVIE_ERR_MSG, BAD_REQ_MOVIE_ERR_MSG, SAME_NAME_MOVIE_ERR_MSG
from api.api_manager import ApiManager


def test_create_movie(movie_data, api_manager: ApiManager):
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.create_movie(movie_data, expected_status=201)
    for key in movie_data:
        assert response.json()[key] == movie_data[key],f'Expected {movie_data[key]}, got {response.json()[key]}'
    movie_id = response.json()['id']
    response_get = api_manager.movie_api.get_movie(movie_id, expected_status=200)
    for key in response.json():
        assert response_get.json()[key] == response.json()[key],\
            f'Expected {response.json()[key]}, got {response_get.json()[key]}'
    api_manager.movie_api.delete_movie(response.json()['id'])

def test_create_movie_with_incorrect_movie_data(api_manager: ApiManager, incorrect_movie_data):
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.create_movie(incorrect_movie_data, expected_status=400)
    response_data = response.json()
    assert response_data['error'] == BAD_REQ_MOVIE_ERR_MSG,\
        f'Expected error: "{BAD_REQ_MOVIE_ERR_MSG}", got "{response_data['error']}"'

def test_create_movie_with_same_name(api_manager: ApiManager, movie_data):
    api_manager.auth_api.authenticate(USER_CREDS)
    response = api_manager.movie_api.create_movie(movie_data)
    response_second = api_manager.movie_api.create_movie(movie_data, expected_status=409)
    response_data = response_second.json()
    assert response_data['message'] == SAME_NAME_MOVIE_ERR_MSG,\
        f'Expected error: "{SAME_NAME_MOVIE_ERR_MSG}", got "{response_data['message']}"'
    api_manager.movie_api.delete_movie(response.json()['id'])

def test_create_movie_unathorized(api_manager: ApiManager, movie_data):
    api_manager.auth_api.unauthenticate()
    response = api_manager.movie_api.create_movie(movie_data, expected_status=401)
    response_data = response.json()
    assert response_data['message'] == UNATHORIZE_MOVIE_ERR_MSG,\
        f'Expected error message: "{UNATHORIZE_MOVIE_ERR_MSG}", got "{response_data['message']}"'