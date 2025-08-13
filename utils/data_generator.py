import random
import string
from faker import Faker
from random import randrange, choice
import pytest

faker = Faker()


class DataGenerator:
    """
    Класс для генерации тестовых данных
    """
    @staticmethod
    def generate_params_for_filters():
        """
        Метод создаёт данные для применения в фильтрах фильмов
        """
        data = []
        for i in range(3):
            max_price = randrange(500, 1000)
            min_price = randrange(0, 1000-max_price)
            location = choice(['MSK', 'SPB'])
            genre_id = choice([23, 12, 14, 6, 10])
            data.append((max_price, min_price, location, genre_id))
        result = data.copy()
        return result


    @staticmethod
    def generate_random_bool(chance=66):
        return faker.boolean(chance)


    @staticmethod
    def generate_random_choice(objects: list):
        return random.choice(objects)


    @staticmethod
    def generate_random_text():
        return faker.text()


    @staticmethod
    def generate_random_int(left, right):
        return faker.random_int(left, right)


    @staticmethod
    def generate_random_movie_name():
        """
        Метод создаёт слуяайное название фильма
        :return:
        """
        return faker.sentence()


    @staticmethod
    def generate_random_email():
        """
        Метод создаёт случайный email
        :return:
        """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_string}@gmail.com"


    @staticmethod
    def generate_random_name():
        """
        Метод создаётся случаное имя и фамилию
        :return:
        """
        return f"{faker.first_name()} {faker.last_name()}"


    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)