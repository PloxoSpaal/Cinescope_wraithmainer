from custom_requester.custom_requester import CustomRequester
from requests import Session
from constants import BASE_URL
from typing import List
from schemas.movie_schema import CreateMovieRequestSchema
from requests import Response
import allure


class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session: Session):
        super().__init__(session=session, base_url=BASE_URL)

    @allure.step("Создание фильма /movies")
    def create_movie(self, movie_data: CreateMovieRequestSchema, expected_status: int = 201) -> Response:
        """
        Создание фильма
        :param movie_data: данные для создания фильма
        :param expected_status: Ожидаемый статус-код
        """
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            expected_status=expected_status
        )

    @allure.step("Получение фильма /movies/{movie_id}")
    def get_movie(self, movie_id: str, expected_status=200) -> Response:
        """
        Получение информации о фильме по ID
        :param movie_id: ID фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f'/movies/{movie_id}',
            expected_status=expected_status
        )

    @allure.step("Получение списка фильмов /movies")
    def get_movies(self, expected_status: int = 200, page_size: int = 10, page: int = 1,
                   min_price: int = 1, max_price: int = 1000, locations: List[str] = ['MSK', 'SPB'],
                   published: bool = True, genre_id: None = None, created_at: str = 'asc') -> Response:
        """
        Получение списка фильмов с фильтрацией.
        :param expected_status: Ожидаемый статус-код.
        :param page_size: Количество фильмов на 1 странице
        :param page: Номер страницы
        :param min_price: Минимальная стоимость фильма
        :param max_price: Максимальная стоимость фильма
        :param locations: Локации места снятия фильмов
        :param published: Статус публикации фильма
        :param genre_id: ID жанра фильма
        :param created_at: Сортировка по дате выхода фильма
        """
        params = {
            'pageSize': page_size,
            'page': page,
            'minPrice': min_price,
            'maxPrice': max_price,
            'locations': locations,
            'published': published,
            'createdAt': created_at
        }

        if genre_id is not None:
            params = params.copy()
        params.update({'genreId': genre_id})

        return self.send_request(
            method="GET",
            endpoint='/movies',
            params=params,
            expected_status=expected_status)

    @allure.step("Получение списка ID фильмов")
    def get_movies_id(self) -> List[str | int]:
        """
        Получение ID фильмов
        """
        response = self.get_movies()
        movies = response['movies']
        ids = list(map(lambda x: x['id'], movies))
        return ids

    @allure.step("Удаление фильма /movies/{movie_id}")
    def delete_movie(self, movie_id: str, expected_status: int = 200) -> Response:
        """
        Метод удаляет фильм по его ID
        :param movie_id: ID фильма
        """
        return self.send_request(
            method="DELETE",
            endpoint=f'/movies/{movie_id}',
            expected_status=expected_status
        )

    @allure.step("Обновление фильма /movies/{movie_id}")
    def update_movie(self, movie_id: str, movie_data: CreateMovieRequestSchema,
                     expected_status: int = 200) -> Response:
        """
        Метод обновляет данные фильма
        :param movie_id: Id фильма
        :param movie_data: Данные для изменения
        :param expected_status: Ожидаемый статус-код
        """
        return self.send_request(
            method="PATCH",
            endpoint=f'/movies/{movie_id}',
            data=movie_data,
            expected_status=expected_status
        )
