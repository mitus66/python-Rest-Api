# Використання офіційного образу Python в якості базового
# Ми використовуємо python:3.11-slim, так як він менший за розміром
FROM python:3.11-slim

# Встановлення змінних середовища для запобігання буферизації виводу Python
# та для використання останньої версії pip
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Встановлення робочої директорії в контейнері
WORKDIR /app

# Копіювання файлу з залежностями та їх встановлення
# Це кешує шар Docker, прискорюючи подальші збірки
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копіювання скрипту для очікування та надання йому прав на виконання
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Копіювання всього іншого коду застосунку в контейнер
COPY . /app

# Відкриття порту 8000, на якому буде працювати Uvicorn
EXPOSE 8000

# Команда для запуску Uvicorn. Цей рядок буде перезаписаний командою з docker-compose.yml
# Залишаємо його для того, щоб образ міг бути запущений без docker-compose
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]