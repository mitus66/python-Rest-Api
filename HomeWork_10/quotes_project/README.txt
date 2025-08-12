1. docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres

2. python manage.py makemigrations authors
3. python manage.py makemigrations quotes
4. python manage.py migrate
5. python migrate_mongo_to_postgres.py

6. python manage.py createsuperuser
7. python manage.py runserver