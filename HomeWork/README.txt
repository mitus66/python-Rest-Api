1. Підключіть Docker, замінюючи на власні значення postgresdbname і mysecretpassword:
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

2. Встановіть psycopg2-binary:
pip install psycopg2-binary

3. Налаштування Alembic та створення міграцій
Установіть alembic:
pip install alembic

    Крок 1: Ініціалізуйте Alembic
    Відкрийте термінал у кореневому каталозі вашого проєкту та виконайте:
    alembic init migrations
    Це створить каталог migrations та файл alembic.ini.

    Крок 2: Відредагуйте alembic.ini
    Відкрийте файл alembic.ini та знайдіть розділ [alembic] та sqlalchemy.url.
    Змініть sqlalchemy.url на ваш рядок підключення до PostgreSQL:
    # alembic.ini
    # ...
    [alembic]
    script_location = migrations
    # ...
    sqlalchemy.url = postgresql://postgres:mysecretpassword@localhost:5432/postgres
    # ...
    Також, у файлі migrations/env.py, вам потрібно буде імпортувати Base з вашого models.py та вказати його для target_metadata.
    Знайдіть функцію run_migrations_online() та змініть її так:

    # migrations/env.py
    # ...
    from models import Base, engine # Додайте цей імпорт
    # ...

    def run_migrations_online():
        """Run migrations in 'online' mode.
        In this scenario we need to create an Engine
        and associate a connection with the context.
        """
        connectable = engine # Використовуйте ваш engine з models.py

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=Base.metadata, # Вкажіть Base.metadata
                # literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )

            with context.begin_transaction():
                context.run_migrations()

    Крок 3: Створіть першу міграцію

    У терміналі виконайте команду:
    alembic revision --autogenerate -m "Create initial tables"
    Це створить новий файл у каталозі migrations/versions/
    (наприклад, xxxxxxxxxxxx_create_initial_tables.py).
    Цей файл міститиме SQL-інструкції для створення ваших таблиць.

    Крок 4: Запустіть міграцію
    У терміналі виконайте:
    alembic upgrade head
    Це застосує міграції до вашої бази даних PostgreSQL, створивши всі таблиці.

4. seed.py - Заповнення бази даних випадковими даними
Цей скрипт використовуватиме Faker та SQLAlchemy сесії для наповнення бази даних.

Встановіть бібліотеку Faker: pip install Faker
Запустіть скрипт з терміналу:
python seed.py
Це заповнить вашу базу даних PostgreSQL.

5. my_select.py - SQL-запити за допомогою SQLAlchemy ORM
Цей файл міститиме 10 функцій, що виконують запити за допомогою SQLAlchemy ORM.

Інструкції для запуску my_select.py:
Запустіть скрипт з терміналу:
python my_select.py
Ви побачите вивід результатів кожного запиту.
Для запитів, які вимагають конкретних імен (викладачів, студентів, предметів, груп),
вам потрібно буде замінити заглушки ('Імя Студента', 'Назва Предмета'тощо)
на реальні значення з вашої заповненої бази даних.
Ви можете отримати ці імена, наприклад, виконавши простий запит
SELECT fullname FROM students LIMIT 1;

# Результат:
1. 5 студентів із найбільшим середнім балом:
('Леонтій Слюсар', Decimal('84.25'))
('Еріка Ковалюк', Decimal('83.78'))
('Василина Данькевич', Decimal('83.67'))
('Анжела Ватаманюк', Decimal('83.25'))
('Абраменко Аліна Борисівна', Decimal('83.00'))

2. Студент з найвищим середнім балом з 'Математика':
('Сніжана Базилевська', Decimal('85.14'))

3. Середній бал у групах з 'Фізика':
('Group A', Decimal('80.41'))
('Group B', Decimal('80.11'))
('Group C', Decimal('78.93'))

4. Середній бал на потоці:
(Decimal('80.33'),)

# Щоб протестувати select_5, select_8, select_9, select_10, вам потрібно буде
# знати реальні імена викладачів та студентів з вашої заповненої бази даних.
# Ви можете запустити seed.py, а потім вручну перевірити таблиці,
# або додати логіку для вибору випадкових імен з бази.

# Приклад виклику з реальними даними (замініть на імена з вашої БД)
# select_5('Олена Коваленко')
# select_6('Group A')
# select_7('Group B', 'Хімія')
# select_8('Іван Петренко')
# select_9('Марія Савченко')
# select_10('Андрій Мельник', 'Олена Коваленко')