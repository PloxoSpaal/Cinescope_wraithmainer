from typing import Any
import allure
from pytest_check import check


@allure.step("Сравнение значений в поле {name}")
def assert_equal(actual: Any, expected: Any, name: str):
    """
    Базовая проверка равенства двух значений, поддерживающих сравнение
    :param actual: Действительное значение
    :param expected: Ожидаемое значение
    :param name: Название сравниваемого поля
    """
    with check('Проверка соответствия типов данных'):
        if not isinstance(actual, type(expected)) and not isinstance(expected, type(actual)):
            raise AssertionError(
                f'Type mismatch in "{name}":\n'
                f'  Expected: {type(expected).__name__}\n'
                f'  Actual:   {type(actual).__name__}')
    assert actual == expected, (
        f'''Incorrect value in "{name}":
            expect "{expected}", got "{actual}"''')