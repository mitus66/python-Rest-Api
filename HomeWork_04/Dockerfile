# Базовий образ з Python
FROM python:3.11-slim

# Встановлення робочої директорії всередині контейнера
WORKDIR /app

# Копіюємо вміст проєкту до контейнера
COPY . .

# Встановлюємо залежності (якщо потрібно)
# RUN pip install -r requirements.txt

# Відкриваємо порти: HTTP (3000) і UDP Socket (5000)
EXPOSE 3000 5000/udp

# Встановлюємо змінну середовища для Python
ENV PYTHONUNBUFFERED=1

# Запуск скрипта
CMD ["python", "main.py"]
