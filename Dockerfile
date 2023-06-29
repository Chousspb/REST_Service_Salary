# Указываем базовый образ
FROM python:3.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости проекта
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Копируем остальные файлы проекта
COPY . /app

# Запускаем приложение при старте контейнера
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
