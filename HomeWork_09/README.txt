Інструкції для запуску:
1. Встановіть необхідні бібліотеки:
pip install scrapy mongoengine pymongo Faker

2. Налаштуйте connect.py: Відкрийте connect.py та обов'язково замініть плейсхолдери YOUR_USERNAME, YOUR_PASSWORD, YOUR_CLUSTER_URL, YOUR_DB_NAME на ваші реальні дані з MongoDB Atlas.

3. Створіть файли та структуру:
Створіть каталог quotes_scraper та його підкаталоги (spiders).
Скопіюйте вміст кожного блоку коду у відповідні файли, дотримуючись структури.
Переконайтеся, що authors.json та quotes.json (які будуть згенеровані) знаходяться в кореневому каталозі проєкту. Якщо вони вже існують, вони будуть перезаписані.

4. Запустіть main.py:
Відкрийте термінал у кореневому каталозі вашого проєкту (де знаходиться main.py та папка quotes_scraper) і запустіть:
python main.py

Що відбудеться:
main.py запустить Scrapy павука.
Павук QuotesSpider обійде сайт quotes.toscrape.com, збере цитати та інформацію про авторів.
JsonWriterPipeline збереже зібрані дані у файлах authors.json та quotes.json у кореневому каталозі.
Після завершення скрапінгу, main.py викличе функції з load_data.py для підключення до MongoDB та завантаження даних з новостворених JSON файлів.
Ваша попередня робота (наприклад, скрипт search_quotes.py) повинна тепер коректно працювати з цими новими даними у вашій хмарній базі даних.

Відповідь:
2025-08-02 11:18:18 [scrapy.core.engine] INFO: Spider closed (finished)

--- Скрапінг завершено. Початок завантаження даних у MongoDB ---
Successfully connected to MongoDB Atlas!
Error: authors.json not found. Skipping author loading.
Error: quotes.json not found. Skipping quote loading.

--- Процес завантаження даних у MongoDB завершено ---
