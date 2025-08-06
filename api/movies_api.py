from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    """
    Класс для работы с API фильмов.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

    def create_movie(self, movie_data, expected_status=201):
        """
        Создание фильма
        :param movie_data: данные для создания фильма
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint="/movies",
            data=movie_data,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
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

    def get_movies(self, expected_status=200, page_size=10, page=1, min_price=1, max_price=1000,
                   locations=['MSK','SPB'], published=True, genre_id=None, created_at='asc'):
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
            'publisghed': published,
            'createdAt': created_at
        }

        if genre_id is not None:
            params = params.copy()
            params.update({'genreId': genre_id})

        return self.send_request(
            method="GET",
            endpoint='/movies',
            params=params,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        """
        Метод удаляет фильм по его ID.
        :param movie_id: ID фильма
        """
        return self.send_request(
            method="DELETE",
            endpoint=f'/movies/{movie_id}',
            expected_status=expected_status
        )

    def update_movie(self, movie_id, movie_data, expected_status=200):
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
