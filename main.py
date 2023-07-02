from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from datetime import datetime, timedelta
import uvicorn
import secrets

# Инициализируем FastAPI и создаем экземпляр шаблонизатора
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# База данных с пользователями и их зарплатами
users_db = {
    "ivan": {"password": "12345", "salary": 50000, "next_raise": "2023-09-01"},
    "vova": {"password": "54321", "salary": 60000, "next_raise": "2023-10-01"},
    "oleg": {"password": "qwerty", "salary": 70000, "next_raise": "2023-11-01"},
    "masha": {"password": "ytrewq", "salary": 80000, "next_raise": "2023-12-01"},
}

# Словарь для хранения активных токенов
active_tokens = {}


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Проверка логина и пароля
    if username in users_db and users_db[username]["password"] == password:
        # Логин и пароль верные
        token = generate_token()  # Генерация токена
        active_tokens[token] = {
            "username": username,
            "created_at": datetime.now()
        }  # Сохранение токена в словаре активных токенов
        return templates.TemplateResponse("token.html", {"request": request, "token": token})
    else:
        # Логин и пароль неверные
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error_message": "Логин или пароль неверные"})


@app.get("/salary", response_class=HTMLResponse)
async def get_salary(request: Request, token: str):
    # Проверяем, что токен действительный и не истек
    if token not in active_tokens:
        return templates.TemplateResponse("wrong.html", {"request": request})

    token_data = active_tokens[token]
    username = token_data["username"]
    created_at = token_data["created_at"]
    elapsed_time = datetime.now() - created_at
    token_lifetime = timedelta(minutes=1)  # Устанавливаем желаемое время жизни токена

    if elapsed_time > token_lifetime:
        del active_tokens[token]  # Удаляем просроченный токен
        return templates.TemplateResponse("expired.html", {"request": request})

    user_data = users_db.get(username)

    if user_data:
        salary = user_data["salary"]
        next_raise = user_data["next_raise"]

        return templates.TemplateResponse("salary.html",
                                          {"request": request, "salary": salary, "next_raise": next_raise})

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Пользователь не найден")


@app.get("/", response_class=HTMLResponse)  # HTMLResponse, чтобы возвращать HTML-страницу
async def index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def generate_token():  # Функция для генерации токена
    example_token = secrets.token_hex(16)
    return example_token


if __name__ == "__main__":  # Запуск приложения
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
