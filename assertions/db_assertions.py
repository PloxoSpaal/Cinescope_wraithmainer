import allure
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, text, Float, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from schemas.db_schema.movie_db_schema import MovieTableDBSchema
from assertions.base_assertions import assert_equal
from schemas.movie_fixture_shema import MovieFixtureSchema


@allure.step("Проверка наличия фильма в БД")
def assert_movie_in_db(session: Session, movie_id: str):
    movie_from_db = session.query(MovieTableDBSchema).filter(MovieTableDBSchema.id == movie_id)
    assert movie_from_db.count() == 1, 'Movie not found in DB'

@allure.step("Проверка данных фильма в БД")
def assert_movie_values_in_db(session: Session, movie: MovieFixtureSchema):
    movies_from_db = session.query(MovieTableDBSchema).filter(MovieTableDBSchema.id == movie.id)
    movie_from_db = movies_from_db.first()
    assert_equal(movie_from_db.id, movie.id, 'id')
    assert_equal(movie_from_db.name, movie.name, 'name')
    assert_equal(movie_from_db.price, movie.price, 'price')
    assert_equal(movie_from_db.description, movie.description, 'description')
    assert_equal(movie_from_db.image_url, movie.image_url, 'image_url')
    assert_equal(movie_from_db.location, movie.location, 'location')
    assert_equal(movie_from_db.published, movie.published, 'published')
    assert_equal(movie_from_db.rating, movie.rating, 'rating')
    assert_equal(movie_from_db.genre_id, movie.genre_id, 'genre_id')
    #assert_equal(movie_from_db.created_at, movie.created_at, 'created_at')

