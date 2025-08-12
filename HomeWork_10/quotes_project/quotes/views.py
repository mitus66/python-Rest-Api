# quotes/views.py
from django.shortcuts import render
from .models import Quote

def index(request):
    # Тепер цей рядок працюватиме, оскільки Djongo "перекладає" запит для MongoDB
    quotes = Quote.objects.all()
    return render(request, 'quotes/index.html', {'quotes': quotes})


# # Тут має бути імпорт вашої моделі Quotes
# # Наприклад: from .models import Quote
#
# def index(request):
#     try:
#         # Цей рядок відповідає за отримання всіх цитат з бази
#         # Замініть його на свій код, який отримує дані з MongoDB
#         # Наприклад, якщо ви використовуєте pymongo:
#         # client = MongoClient(settings.MONGO_DB_CONNECTION_STRING)
#         # db = client[settings.MONGO_DB_NAME]
#         # quotes = list(db.quotes.find({}))
#
#         # Для прикладу, уявімо, що наша модель має метод .objects.all()
#         quotes = Quote.objects.all()
#
#         # Якщо в колекції немає даних, ця змінна буде порожнім QuerySet
#     except Exception as e:
#         # Обробка помилок підключення або запиту до бази
#         quotes = []
#         print(f"Помилка при отриманні даних з MongoDB: {e}")
#
#     # Передача змінної `quotes` у контекст шаблону
#     return render(request, 'quotes/index.html', {'quotes': quotes})

