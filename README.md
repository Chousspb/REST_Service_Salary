# Инструкция по запуску сервиса и взаимодействию с проектом

## Требования

Для запуска данного сервиса вам понадобится установленный Python версии 3.10 или выше, а также инструмент Poetry.

## Установка инструмента Poetry

1. Установите инструмент Poetry, следуя официальной документации: [Poetry Installation Guide](https://python-poetry.org/docs/#installation)

## Запуск сервиса

1. Склонируйте репозиторий с проектом:

   ```bash
   git clone https://gitlab.com/Chousspb/REST_Service_Salary.git

2. Перейдите в директорию проекта:
cd repository

3. Установите зависимости с использованием Poetry:
poetry install

4. Запустите сервис с помощью Poetry:
poetry run uvicorn main:app --host 0.0.0.0 --port 8000

Взаимодействие с сервисом:
Откройте веб-браузер и перейдите по адресу http://0.0.0.0:8000.
Введите логин и пароль в форме на странице входа и нажмите кнопку "Войти".
При успешной авторизации вы будете перенаправлены на страницу с токеном.
Чтобы получить данные о зарплате, нажмите на ссылку "Данные о зарплате"
Если токен действителен, вы увидите страницу с информацией о зарплате и дате повышения.

# Запуск сервиса через контейнер Docker

1.  Склонируйте репозиторий с проектом:

   ```bash
   git clone https://gitlab.com/Chousspb/REST_Service_Salary.git

2. Перейдите в директорию проекта:

   ```bash
   cd repository

4. Открыть терминал и выполнить следующую команду для сборки и запуска контейнера:

   ```bash
   docker-compose up --build

6. Docker соберет образ и запустит контейнер с вашим проектом. Вы увидит вывод в терминале, указывающий на запуск сервера FastAPI.
Теперь можно получить доступ к проекту, открыв веб-браузер и перейдя по адресу http://0.0.0.0:8000. 
