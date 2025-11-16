# 1. Базовий образ
FROM python:3.11-slim as addressbook-cli

# 2. Робоча директорія всередині контейнера
WORKDIR /app

# 3. Встановлюємо Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# 4. Копіюємо файли до контейнера
COPY pyproject.toml poetry.lock* ./
COPY . .

# 5. Конфігурація Poetry (відключає створення віртуального оточення)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

# 6. Вказуємо команду запуску застосунку
CMD ["python", "addressbook.py"]
