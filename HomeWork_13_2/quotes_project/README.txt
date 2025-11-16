1. docker run --name postgres13 -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres

2. cd ./quotes_project
3. python manage.py makemigrations authors
4. python manage.py makemigrations quotes
5. python manage.py migrate
6. python migrate_mongo_to_postgres.py

7. python manage.py createsuperuser
8. python manage.py runserver

9. python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'