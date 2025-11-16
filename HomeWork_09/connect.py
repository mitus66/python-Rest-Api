from mongoengine import connect
import os

# Отримайте URL підключення з змінної оточення або встановіть за замовчуванням
# Рекомендується використовувати змінні оточення для конфіденційних даних
# ЗАМІНІТЬ ЦІ ПЛЕЙСХОЛДЕРИ НА ВАШІ РЕАЛЬНІ ДАНІ
# MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER_URL/YOUR_DB_NAME?retryWrites=true&w=majority")
MONGO_URI = os.getenv("mongodb+srv://mitus66:Alaska725@cluster0.qzzbjox.mongodb.net/mongodb_1?retryWrites=true&w=majority")

def connect_db():
    """Встановлює з'єднання з базою даних MongoDB Atlas."""
    try:
        connect(host=MONGO_URI)
        print("Successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        # Можна додати sys.exit(1) тут, якщо з'єднання є критичним
