from enum import Enum
import os


BASE_URL = 'https://api.dev-cinescope.coconutqa.ru'
AUTH_BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru'
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
OK_STATUS_CODE = [200, 201]
REGISTER_ENDPOINT = '/register'
USER_CREDS = (os.getenv('SUPER_ADMIN_USERNAME'), os.getenv('SUPER_ADMIN_PASSWORD'))
LOGIN_ENDPOINT = '/login'
AUTH_ERR_MSG = 'Неверный логин или пароль'
UNATHORIZED_MOVIE_ERR_MSG = 'Unauthorized'
BAD_REQ_MOVIE_ERR_MSG = 'Bad Request'
SAME_NAME_MOVIE_ERR_MSG = "Фильм с таким названием уже существует"
NOT_FOUND_MOVIE_ERR_MSG = "Фильм не найден"
FORBIDDEN_MOVIE_ERR_MSG = "Forbidden resource"
GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'

class Roles(str, Enum):

    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

    def __str__(self):
        return self.value
