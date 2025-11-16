import json
import os
from connect import connect_db
from models import Author, Quote

# Шляхи до JSON файлів
AUTHORS_FILE = 'authors.json'
QUOTES_FILE = 'quotes.json'


def load_authors():
    """Завантажує дані авторів з JSON файлу в колекцію authors."""
    if not os.path.exists(AUTHORS_FILE):
        print(f"Error: {AUTHORS_FILE} not found.")
        return

    with open(AUTHORS_FILE, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    print(f"Loading {len(authors_data)} authors...")
    for author_data in authors_data:
        try:
            author = Author(**author_data)
            author.save()
            print(f"  Saved author: {author.fullname}")
        except Exception as e:
            print(f"  Error saving author {author_data.get('fullname', 'N/A')}: {e}")
            # Це може бути помилка унікальності, якщо ви запускаєте скрипт кілька разів
            # і автор вже існує.


def load_quotes():
    """Завантажує дані цитат з JSON файлу в колекцію quotes."""
    if not os.path.exists(QUOTES_FILE):
        print(f"Error: {QUOTES_FILE} not found.")
        return

    with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)

    print(f"Loading {len(quotes_data)} quotes...")
    for quote_data in quotes_data:
        author_name = quote_data.pop('author')  # Видаляємо ім'я автора зі словника цитати
        author = Author.objects(fullname=author_name).first()  # Знаходимо автора за ім'ям

        if author:
            try:
                quote = Quote(author=author, **quote_data)  # Присвоюємо ReferenceField
                quote.save()
                print(f"  Saved quote by {author.fullname}")
            except Exception as e:
                print(f"  Error saving quote by {author_name}: {e}")
        else:
            print(f"  Author '{author_name}' not found for quote: {quote_data.get('quote', 'N/A')[:50]}...")


if __name__ == "__main__":
    connect_db()  # Встановлюємо з'єднання з БД

    # Завантажуємо авторів першими, оскільки цитати на них посилаються
    load_authors()
    load_quotes()
    print("\nData loading complete.")
