import os
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Додаємо шлях до проекту Scrapy до PYTHONPATH
# Це дозволить імпортувати павуків та налаштування
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'quotes_scraper'))

# Імпортуємо павука
from quotes_scraper.spiders.quotes_spider import QuotesSpider

# Імпортуємо функції завантаження даних
from load_data import load_authors_to_db, load_quotes_to_db
from connect import connect_db  # Для підключення до MongoDB перед завантаженням


def run_scraper_and_load_data():
    """
    Запускає Scrapy павука для скрапінгу даних,
    потім завантажує отримані JSON файли в MongoDB.
    """
    print("--- Початок процесу скрапінгу ---")

    # Отримуємо налаштування Scrapy проекту
    settings = get_project_settings()

    # Ініціалізуємо CrawlerProcess з налаштуваннями
    process = CrawlerProcess(settings)

    # Додаємо павука до процесу
    process.crawl(QuotesSpider)

    # Запускаємо процес скрапінгу (блокуючий виклик)
    process.start()

    print("\n--- Скрапінг завершено. Початок завантаження даних у MongoDB ---")

    # Підключаємося до MongoDB
    connect_db()

    # Завантажуємо дані авторів
    load_authors_to_db()

    # Завантажуємо дані цитат
    load_quotes_to_db()

    print("\n--- Процес завантаження даних у MongoDB завершено ---")


if __name__ == "__main__":
    run_scraper_and_load_data()
