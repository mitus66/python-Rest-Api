import json
import os
from connect import connect_db
from models import Author, Quote

# Шляхи до JSON файлів
AUTHORS_FILE = 'authors.json'
QUOTES_FILE = 'quotes.json'


def load_authors_to_db():
    """Завантажує дані авторів з JSON файлу в колекцію authors."""
    if not os.path.exists(AUTHORS_FILE):
        print(f"Error: {AUTHORS_FILE} not found. Skipping author loading.")
        return

    with open(AUTHORS_FILE, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    print(f"Loading {len(authors_data)} authors to MongoDB...")
    for author_data in authors_data:
        try:
            # Використовуємо update_one з upsert=True, щоб уникнути дублікатів
            # або оновити існуючого автора, якщо він вже є
            Author.objects(fullname=author_data['fullname']).update_one(upsert=True, **author_data)
            print(f"  Processed author: {author_data['fullname']}")
        except Exception as e:
            print(f"  Error processing author {author_data.get('fullname', 'N/A')}: {e}")


def load_quotes_to_db():
    """Завантажує дані цитат з JSON файлу в колекцію quotes."""
    if not os.path.exists(QUOTES_FILE):
        print(f"Error: {QUOTES_FILE} not found. Skipping quote loading.")
        return

    with open(QUOTES_FILE, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)

    print(f"Loading {len(quotes_data)} quotes to MongoDB...")
    for quote_data in quotes_data:
        author_name = quote_data.pop('author')  # Видаляємо ім'я автора зі словника цитати
        author = Author.objects(fullname=author_name).first()  # Знаходимо автора за ім'ям

        if author:
            try:
                # Перевіряємо, чи цитата вже існує, щоб уникнути дублікатів
                # Можна використовувати комбінацію автора та тексту цитати як унікальний ключ
                existing_quote = Quote.objects(author=author, quote=quote_data['quote']).first()
                if not existing_quote:
                    quote = Quote(author=author, **quote_data)  # Присвоюємо ReferenceField
                    quote.save()
                    print(f"  Saved quote by {author.fullname}")
                else:
                    print(f"  Quote by {author.fullname} already exists: {quote_data['quote'][:30]}...")
            except Exception as e:
                print(f"  Error saving quote by {author_name}: {e}")
        else:
            print(f"  Author '{author_name}' not found for quote: {quote_data.get('quote', 'N/A')[:50]}... Skipping.")


if __name__ == "__main__":
    connect_db()  # Встановлюємо з'єднання з БД

    # Завантажуємо авторів першими, оскільки цитати на них посилаються
    load_authors_to_db()
    load_quotes_to_db()
    print("\nData loading complete.")
