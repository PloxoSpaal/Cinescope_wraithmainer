import pytest
from constants import NOT_FOUND_MOVIE_ERR_MSG
from api.api_manager import ApiManager


def test_get_movies(api_manager: ApiManager):
    response = api_manager.movie_api.get_movies()
    response_data = response.json()
    assert len(response_data['movies']) == 10, f'Expected 10 movies in page, got {len(response_data['movies'])}'
    assert len(response_data['movies']) == response_data['pageSize'],\
        f'Expected {response_data['pageSize']} movies in page, got {len(response_data["movies"])}'

def test_get_movies_with_filter(api_manager: ApiManager):
    min_price = 700
    max_price = 1000
    page_size = 5
    response = api_manager.movie_api.get_movies(min_price=min_price,max_price=max_price, page_size=5)
    response_data = response.json()
    assert len(response_data['movies']) == page_size, f'Expected {page_size} movies in page, got {len(response_data['movies'])}'
    assert len(response_data['movies']) == response_data['pageSize'],\
        f'Expected {response_data['pageSize']} movies in page, got {len(response_data["movies"])}'
    movies = response_data['movies']
    for movie in movies:
        assert min_price <= movie['price'] <= max_price, 'Price dont match filters'

def test_get_movie(api_manager: ApiManager, create_movie_fixture):
    response = api_manager.movie_api.get_movie(create_movie_fixture['id'])
    response_data = response.json()
    for key in create_movie_fixture:
        assert response_data[key] == create_movie_fixture[key],\
            f'Expected {create_movie_fixture[key]}, got {response_data[key]} in {key}'

def test_get_movie_not_found(api_manager: ApiManager):
    response = api_manager.movie_api.get_movie(movie_id=0, expected_status=404)
    response_data = response.json()
    assert response_data['message'] == NOT_FOUND_MOVIE_ERR_MSG,\
        f'Expected message: {NOT_FOUND_MOVIE_ERR_MSG}, got {response_data["message"]}'