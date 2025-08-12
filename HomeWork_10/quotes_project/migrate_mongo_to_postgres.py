# migrate_mongo_to_postgres.py
import os
import django
from dotenv import load_dotenv
from pymongo import MongoClient
import sys

# Додаємо кореневу директорію проєкту до шляху
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Налаштовуємо Django
# Це критично важливий крок для доступу до Django ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

# Імпортуємо ваші моделі Django
from quotes.models import Author, Quote

mongo_uri = os.getenv("MONGO_URI")

if not mongo_uri:
    print("Помилка: Не вдалося завантажити змінну середовища MONGO_URI з .env файлу.")
    exit()

print("Змінні успішно завантажені:")
print(f"MongoDB URI: {mongo_uri}")

# Підключення до MongoDB
try:
    client = MongoClient(mongo_uri)
    mongo_db = client.get_database("mongodb_1")
    print("Успішне підключення до MongoDB.")
except Exception as e:
    print(f"Помилка підключення до MongoDB: {e}")
    exit()

# Отримуємо дані з MongoDB
mongo_authors = list(mongo_db.authors.find())
mongo_quotes = list(mongo_db.quotes.find())

# Словник для збереження відповідності MongoDB full_name -> Django Author object
django_authors = {}

print("Починаємо міграцію даних...")

# Спочатку переносимо авторів
print("Міграція авторів...")
for author_data in mongo_authors:
    fullname = author_data.get('fullname')
    if fullname and fullname not in django_authors:
        author, created = Author.objects.get_or_create(
            fullname=fullname,
            defaults={
                'born_date': author_data.get('born_date'),
                'born_location': author_data.get('born_location'),
                'description': author_data.get('description'),
            }
        )
        django_authors[fullname] = author
        if created:
            print(f"Додано нового автора: {fullname}")
        else:
            print(f"Автор вже існує, оновлено: {fullname}")

# Тепер переносимо цитати
print("Міграція цитат...")
for quote_data in mongo_quotes:
    quote_text = quote_data.get('quote')
    author_name = quote_data.get('author')
    tags = quote_data.get('tags', [])

    if quote_text and author_name:
        author_obj = django_authors.get(author_name)
        if author_obj:
            # Перевіряємо, чи цитата вже існує, щоб уникнути дублювання
            quote, created = Quote.objects.get_or_create(
                text=quote_text,  # Змінено з 'quote' на 'text'
                defaults={
                    'author': author_obj,
                    'tags': ','.join(tags),
                }
            )
            if created:
                print(f"Додано нову цитату для автора {author_name}")
            else:
                print(f"Цитата вже існує, оновлено для автора {author_name}")
        else:
            print(f"Попередження: Автор '{author_name}' для цитати не знайдений у PostgreSQL. Цитату пропущено.")

print("Міграція даних успішно завершена.")


# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, text, Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import declarative_base, relationship, Session
# from pymongo import MongoClient
# import re
#
# # Завантажуємо змінні середовища з .env файлу
# load_dotenv()
#
# mongo_uri = os.getenv("MONGO_URI")
# postgres_uri = os.getenv("POSTGRES_URI")
#
# # Якщо POSTGRES_URI не знайдено, спробуємо зібрати його з окремих змінних
# if not postgres_uri:
#     postgres_db = os.getenv("POSTGRES_DB")
#     postgres_user = os.getenv("POSTGRES_USER")
#     postgres_password = os.getenv("POSTGRES_PASSWORD")
#     postgres_host = os.getenv("POSTGRES_HOST")
#     postgres_port = os.getenv("POSTGRES_PORT")
#
#     if all([postgres_db, postgres_user, postgres_password, postgres_host, postgres_port]):
#         postgres_uri = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
#         print("POSTGRES_URI успішно зібрано з окремих змінних.")
#     else:
#         print("Помилка: Не вдалося зібрати POSTGRES_URI. Переконайтеся, що всі необхідні змінні (POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT) визначені у .env.")
#         exit()
#
# if not mongo_uri or not postgres_uri:
#     print("Помилка: Не вдалося завантажити змінні середовища. Переконайтеся, що MONGO_URI та POSTGRES_URI (або його компоненти) визначені у .env файлі.")
#     exit()
#
# print("Змінні успішно завантажені:")
# print(f"MongoDB URI: {mongo_uri}")
# print(f"PostgreSQL URI: {postgres_uri}")
#
# # Підключення до MongoDB
# try:
#     client = MongoClient(mongo_uri)
#     mongo_db = client.get_database("mongodb_1")
#     print("Успішне підключення до MongoDB")
# except Exception as e:
#     print(f"Помилка підключення до MongoDB: {e}")
#     exit()
#
# # Підключення до PostgreSQL та створення бази даних, якщо її немає
# try:
#     db_name = re.search(r"\/([^\/?]+)(?:\?|$)", postgres_uri).group(1)
#     base_postgres_uri = postgres_uri.replace(f"/{db_name}", "/postgres")
#
#     temp_engine = create_engine(base_postgres_uri, isolation_level="AUTOCOMMIT")
#     with temp_engine.connect() as conn:
#         result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
#         if not result.scalar():
#             print(f"База даних '{db_name}' не знайдена. Створюємо...")
#             conn.execute(text(f"CREATE DATABASE {db_name}"))
#             print(f"Базу даних '{db_name}' успішно створено.")
#
#     engine = create_engine(postgres_uri)
#     Base = declarative_base()
#
#
#     class Author(Base):
#         __tablename__ = 'authors'
#         id = Column(Integer, primary_key=True)
#         fullname = Column(String(250), nullable=False)
#         born_date = Column(String(50))
#         born_location = Column(String(250))
#         description = Column(Text)
#         quotes = relationship("Quote", back_populates="author")
#
#
#     class Quote(Base):
#         __tablename__ = 'quotes'
#         id = Column(Integer, primary_key=True)
#         quote = Column(Text, nullable=False)
#         author_id = Column(Integer, ForeignKey('authors.id'))
#         tags = Column(String(250))
#         author = relationship("Author", back_populates="quotes")
#
#
#     print("Очищення старих таблиць...")
#     with engine.connect() as conn:
#         # Спочатку видаляємо залежні таблиці або таблиці з зовнішніми ключами
#         # Видаляємо таблицю quotes_tags, якщо вона існує (щоб уникнути помилок залежностей)
#         conn.execute(text("DROP TABLE IF EXISTS quotes_tags;"))
#         # Тепер можна безпечно видалити таблицю quotes
#         conn.execute(text("DROP TABLE IF EXISTS quotes;"))
#         conn.execute(text("DROP TABLE IF EXISTS authors;"))
#         conn.commit()
#
#     print("Створюємо нові таблиці...")
#     # Потім створюємо таблиці з оновленою структурою
#     Base.metadata.create_all(engine)
#
#     print("Успішне підключення та створення таблиць в PostgreSQL")
#
# except Exception as e:
#     print(f"Помилка підключення до PostgreSQL або створення таблиць: {e}")
#     exit()
#
# # Отримуємо дані з MongoDB
# mongo_authors = list(mongo_db.authors.find())
# mongo_quotes = list(mongo_db.quotes.find())
#
# # Створюємо словник для зберігання авторів, виправляючи помилку з '_id'
# authors_map = {}
# for author in mongo_authors:
#     author_data = author.copy()
#     author_data.pop('_id', None)
#     authors_map[author_data['fullname']] = Author(**author_data)
#
# # Створюємо об'єкти Quote, також виправляючи помилку з '_id'
# quotes = []
# for quote in mongo_quotes:
#     quote_data = quote.copy()
#     quote_data.pop('_id', None)
#
#     author_name = quote_data.pop('author')
#
#     author_obj = authors_map.get(author_name)
#     if author_obj:
#         if isinstance(quote_data.get('tags'), list):
#             quote_data['tags'] = ','.join(quote_data['tags'])
#
#         quote_data['author'] = author_obj
#         quotes.append(Quote(**quote_data))
#     else:
#         print(f"Попередження: Автор '{author_name}' для цитати не знайдений.")
#
# # Запис даних у PostgreSQL
# with Session(engine) as session:
#     try:
#         session.add_all(authors_map.values())
#         session.commit()
#         session.add_all(quotes)
#         session.commit()
#         print("Міграція даних успішно завершена.")
#     except Exception as e:
#         session.rollback()
#         print(f"Помилка під час міграції: {e}")
#     finally:
#         session.close()


# # migrate_data.py
#
# import os
# import django
# from dotenv import load_dotenv
# from pymongo import MongoClient
#
# # Налаштовуємо середовище Django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
# django.setup()
#
# # Імпортуємо моделі після налаштування Django
# from quotes.models import Author, Quote
#
# # Завантажуємо змінні оточення
# load_dotenv()
# mongo_uri = os.getenv('MONGO_URI')
#
# if not mongo_uri:
#     print("Помилка: Змінна MONGO_URI не знайдена у файлі .env")
#     exit()
#
# # Підключаємося до MongoDB
# try:
#     client = MongoClient(mongo_uri)
#     db = client.get_database()  # Отримуємо доступ до основної бази даних
#     print("Успішно підключено до MongoDB.")
# except Exception as e:
#     print(f"Помилка підключення до MongoDB: {e}")
#     exit()
#
#
# def migrate_data():
#     """
#     Мігрує дані з колекцій MongoDB 'authors' та 'quotes'
#     до моделей Django в PostgreSQL.
#     """
#     print("Починаю міграцію даних...")
#
#     # Переносимо авторів
#     authors_collection = db['authors']
#     authors_data = authors_collection.find()
#
#     # Використовуємо словник для зберігання відповідності ID з MongoDB до ID з PostgreSQL
#     author_id_map = {}
#
#     for mongo_author in authors_data:
#         # Створюємо або оновлюємо автора в PostgreSQL
#         django_author, created = Author.objects.get_or_create(
#             fullname=mongo_author['fullname'],
#             defaults={
#                 'born_date': mongo_author.get('born_date', ''),
#                 'born_location': mongo_author.get('born_location', ''),
#                 'description': mongo_author.get('description', '')
#             }
#         )
#         if created:
#             print(f"Створено автора: {django_author.fullname}")
#         else:
#             print(f"Автор вже існує: {django_author.fullname}")
#
#         author_id_map[str(mongo_author['_id'])] = django_author
#
#     # Переносимо цитати
#     quotes_collection = db['quotes']
#     quotes_data = quotes_collection.find()
#
#     for mongo_quote in quotes_data:
#         # Отримуємо автора з PostgreSQL, використовуючи мапу
#         author_id = str(mongo_quote['author'])
#         django_author = author_id_map.get(author_id)
#
#         if not django_author:
#             print(f"Помилка: Автор з ID {author_id} не знайдений. Пропускаю цитату.")
#             continue
#
#         # Зберігаємо теги як рядок, розділений комою
#         tags_str = ','.join(mongo_quote.get('tags', []))
#
#         # Створюємо цитату в PostgreSQL
#         django_quote, created = Quote.objects.get_or_create(
#             quote=mongo_quote['quote'],
#             defaults={
#                 'author': django_author,
#                 'tags': tags_str
#             }
#         )
#         if created:
#             print(f"Створено цитату: {django_quote.quote[:30]}...")
#
#     print("Міграція даних завершена.")
#
#
# if __name__ == "__main__":
#     migrate_data()
