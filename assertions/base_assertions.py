from typing import Any
import allure


@allure.step("Сравнение значений в поле {name}")
def assert_equal(actual: Any, expected: Any, name: str):
    assert actual == expected, (
        f'''Incorrect value in "{name}":
            expect "{expected}", got "{actual}"'''
    )