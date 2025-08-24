import datetime
from fastapi import FastAPI, HTTPException

from _test_service.mock_services import DateTimeRequest
import allure

app = FastAPI()
russian_holidays = {
    "01-01": "Новый год",
    "01-07": "Рождество Христово",
    "02-23": "День защитника Отечества",
    "03-08": "Международный женский день",
    "05-01": "Праздник Весны и Труда",
    "05-09": "День Победы",
    "06-12": "День России",
    "11-04": "День народного единства",
    "12-31": "Канун Нового года"}


@allure.step('POST-запрос на сервис /what_is_today')
@app.post("/what_is_today")
def what_is_today(request: DateTimeRequest):
    """
    Преобразование даты в праздник
    :param request: Запрос клиента с датой и временем
    :return: Ответ JSON: {"message": holiday}
    """
    try:
        date_str = request.currentDateTime
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%MZ")
        month_day = date_obj.strftime("%m-%d")
        holiday = russian_holidays.get(month_day, "Сегодня нет праздников в России.")
        return {"message": holiday}
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Некорректный формат даты. Используйте формат 'YYYY-MM-DDTHH:MMZ'.")


@allure.step('Пинг сервиса /what_is_today')
@app.get("/ping")
def ping():
    """
    Ответ сервера для подтверждения его работоспособности
    :return: Текст с ответным сообщением
    """
    return "PONG!"


# Запуск сервера
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=16002)
