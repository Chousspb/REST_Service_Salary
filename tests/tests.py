import pytest
from fastapi.testclient import TestClient
from main import app, generate_token

client = TestClient(app)

# Тест на успешную аутентификацию с правильными учетными данными
def test_successful_authentication():
    response = client.post("/login", data={"username": "john", "password": "secret"})
    assert response.status_code == 200
    assert "Your Token:" in response.text

# Тест на неудачную аутентификацию с неправильными учетными данными
def test_failed_authentication():
    response = client.post("/login", data={"username": "john", "password": "wrong_password"})
    assert response.status_code == 200
    assert "Логин или пароль неверные" in response.text

# Тест на отображение страницы логина после неудачной аутентификации
def test_login_page_after_failed_authentication():
    response = client.post("/login", data={"username": "john", "password": "wrong_password"})
    assert response.status_code == 200
    assert "Login Page" in response.text

# Тест на доступ к данным о зарплате с действительным токеном
def test_access_salary_with_valid_token():
    valid_token = generate_token()
    response = client.get("/salary", params={"token": valid_token})
    assert response.status_code == 200
    assert "Salary" in response.text

# Тест на доступ к данным о зарплате без токена (ожидается ошибка 401 Unauthorized)
def test_access_salary_without_token():
    response = client.get("/salary")
    assert response.status_code == 401
    assert "Invalid token" in response.text

# Тест на доступ к данным о зарплате с недействительным токеном (ожидается ошибка 401 Unauthorized)
def test_access_salary_with_invalid_token():
    invalid_token = "invalid_token"
    response = client.get("/salary", params={"token": invalid_token})
    assert response.status_code == 401
    assert "Invalid token" in response.text

# Тест на доступ к данным о зарплате с токеном, связанным с несуществующим пользователем (ожидается ошибка 404 Not Found)
def test_access_salary_with_token_for_nonexistent_user():
    non_existent_token = generate_token()
    response = client.get("/salary", params={"token": non_existent_token})
    assert response.status_code == 404
    assert "User not found" in response.text

# Тест на генерацию токена (проверка типа и длины токена)
def test_generate_token():
    token = generate_token()
    assert isinstance(token, str)
    assert len(token) == 32

# Тест на отображение страницы логина
def test_login_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Login Page" in response.text

# Тест на отображение страницы с данными о зарплате
def test_salary_page():
    valid_token = generate_token()
    response = client.get("/salary", params={"token": valid_token})
    assert response.status_code == 200
    assert "Salary" in response.text
