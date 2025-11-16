# import sys
# from connect import connect_db
# from models import Author, Quote
#
# def search_quotes():
#     """Реалізує нескінченний цикл для пошуку цитат за командами."""
#     print("Welcome to the Quote Search CLI!")
#     print("Available commands:")
#     print("  name: <author_name>    - Find all quotes by an author.")
#     print("  tag: <tag_name>       - Find all quotes with a specific tag.")
#     print("  tags: <tag1>,<tag2>   - Find all quotes with any of the specified tags (comma-separated, no spaces).")
#     print("  exit                  - Exit the script.")
#     print("\n")
#
#     while True:
#         command_input = input("Enter command: ").strip()
#
#         if command_input.lower() == 'exit':
#             print("Exiting Quote Search CLI. Goodbye!")
#             break
#
#         parts = command_input.split(':', 1)
#         if len(parts) != 2:
#             print("Invalid command format. Please use 'command: value'.")
#             continue
#
#         command_type = parts[0].strip().lower()
#         command_value = parts[1].strip()
#
#         quotes = []
#         try:
#             if command_type == 'name':
#                 author = Author.objects(fullname__iexact=command_value).first() # __iexact для регістронезалежного пошуку
#                 if author:
#                     quotes = Quote.objects(author=author)
#                 else:
#                     print(f"Author '{command_value}' not found.")
#             elif command_type == 'tag':
#                 quotes = Quote.objects(tags__iexact=command_value) # __iexact для регістронезалежного пошуку тегів
#             elif command_type == 'tags':
#                 tags_list = [tag.strip() for tag in command_value.split(',')]
#                 quotes = Quote.objects(tags__in=tags_list) # Пошук цитат, що містять будь-який з тегів
#             else:
#                 print("Unknown command type. Please use 'name', 'tag', 'tags', or 'exit'.")
#                 continue
#
#             if quotes:
#                 print(f"\n--- Results for '{command_input}' ---")
#                 for i, quote in enumerate(quotes):
#                     print(f"{i+1}. {quote.quote} - {quote.author.fullname} (Tags: {', '.join(quote.tags)})")
#                 print("------------------------------------")
#             else:
#                 print(f"No quotes found for '{command_input}'.")
#
#         except Exception as e:
#             print(f"An error occurred during search: {e}")
#
# if __name__ == "__main__":
#     connect_db() # Встановлюємо з'єднання з БД
#     search_quotes()

import sys
import json
import redis
from connect import connect_db
from models import Author, Quote

# Підключення до Redis
try:
    # Припускаємо, що Redis працює на localhost:6379, база даних за замовчуванням db=0
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.ping()  # Перевірка з'єднання
    print("Підключено до кешу Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Не вдалося підключитися до Redis: {e}. Кешування буде вимкнено.")
    r = None  # Вимкнути кешування, якщо з'єднання не вдалося


def search_quotes():
    """Реалізує нескінченний цикл для пошуку цитат за командами."""
    print("Ласкаво просимо до CLI пошуку цитат!")
    print("Доступні команди:")
    print(
        "  name: <ім'я_автора>    - Знайти всі цитати за автором (підтримує часткове співпадіння, наприклад, 'name:al').")
    print(
        "  tag: <назва_тега>       - Знайти всі цитати з певним тегом (підтримує часткове співпадіння, наприклад, 'tag:li').")
    print("  tags: <тег1>,<тег2>   - Знайти всі цитати, де є будь-який із зазначених тегів (через кому, без пробілів).")
    print("  exit                  - Завершити виконання скрипту.")
    print("\n")

    while True:
        command_input = input("Введіть команду: ").strip()

        if command_input.lower() == 'exit':
            print("Вихід з CLI пошуку цитат. До побачення!")
            break

        parts = command_input.split(':', 1)
        if len(parts) != 2:
            print("Невірний формат команди. Будь ласка, використовуйте 'команда: значення'.")
            continue

        command_type = parts[0].strip().lower()
        command_value = parts[1].strip()

        display_quotes_data = []  # Список словників для відображення

        # --- Логіка кешування ---
        cache_key = f"{command_type}:{command_value}"
        cached_result = None
        if r:
            try:
                cached_result = r.get(cache_key)
            except Exception as e:
                print(f"Помилка читання з кешу Redis: {e}")
                cached_result = None  # Вважаємо, що не знайдено в кеші

        if cached_result:
            print(f"Отримання результатів з кешу для '{command_input}'...")
            display_quotes_data = json.loads(cached_result.decode('utf-8'))
        else:
            # --- Логіка запиту до MongoDB ---
            quotes_from_db = []
            try:
                if command_type == 'name':
                    # Використовуємо __iregex для часткового та регістронезалежного пошуку
                    author = Author.objects(fullname__iregex=command_value).first()
                    if author:
                        quotes_from_db = Quote.objects(author=author)
                    else:
                        print(f"Автора, що відповідає '{command_value}', не знайдено.")
                elif command_type == 'tag':
                    # Використовуємо __iregex для часткового та регістронезалежного пошуку тегів
                    quotes_from_db = Quote.objects(tags__iregex=command_value)
                elif command_type == 'tags':
                    tags_list = [tag.strip() for tag in command_value.split(',')]
                    # tags__in вже обробляє логіку OR для кількох тегів
                    quotes_from_db = Quote.objects(tags__in=tags_list)
                else:
                    print("Невідомий тип команди. Будь ласка, використовуйте 'name', 'tag', 'tags' або 'exit'.")
                    continue  # Продовжуємо до наступної ітерації циклу

            except Exception as e:
                print(f"Виникла помилка під час пошуку в MongoDB: {e}")
                continue  # Продовжуємо до наступної ітерації циклу

            if quotes_from_db:
                # Підготовка даних для відображення та кешування
                for quote_obj in quotes_from_db:
                    display_quotes_data.append({
                        'quote_text': quote_obj.quote,
                        'author_name': quote_obj.author.fullname,
                        'tags': quote_obj.tags
                    })
                # Кешування результатів, якщо Redis підключено
                if r:
                    try:
                        # Кешування на 1 годину (3600 секунд)
                        r.setex(cache_key, 3600, json.dumps(display_quotes_data, ensure_ascii=False))
                        print(f"Результати для '{command_input}' кешовано.")
                    except Exception as e:
                        print(f"Помилка запису в кеш Redis: {e}")

        # --- Відображення результатів ---
        if display_quotes_data:
            print(f"\n--- Результати для '{command_input}' ---")
            for i, quote_data in enumerate(display_quotes_data):
                print(
                    f"{i + 1}. {quote_data['quote_text']} - {quote_data['author_name']} (Теги: {', '.join(quote_data['tags'])})")
            print("------------------------------------")
        else:
            # Це повідомлення вже обробляється певними типами команд, якщо автора/тег не знайдено
            # але також слугує загальним "без результатів", якщо запит повернув порожній результат.
            # Уникаємо подвійного виведення, якщо конкретне повідомлення 'не знайдено' вже було виведено
            if command_type not in ['name', 'tag']:  # Виводимо тільки якщо не оброблено конкретним 'не знайдено' вище
                print(f"Цитат не знайдено для '{command_input}'.")


if __name__ == "__main__":
    connect_db()  # Встановлюємо з'єднання з БД
    search_quotes()
