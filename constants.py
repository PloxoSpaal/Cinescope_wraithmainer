BASE_URL = 'https://api.dev-cinescope.coconutqa.ru'
AUTH_BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru'
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
USERNAME = 'api1@gmail.com'
PASSWORD = 'asdqwe123Q'
USER_CREDS = (USERNAME, PASSWORD)
OK_STATUS_CODE = [200, 201]
REGISTER_ENDPOINT = '/register'
LOGIN_ENDPOINT = '/login'
AUTH_ERR_MSG = 'Неверный логин или пароль'
UNATHORIZE_MOVIE_ERR_MSG = 'Unauthorized'
BAD_REQ_MOVIE_ERR_MSG = 'Bad Request'
SAME_NAME_MOVIE_ERR_MSG = "Фильм с таким названием уже существует"
NOT_FOUND_MOVIE_ERR_MSG = "Фильм не найден"