1. Run Docker
docker-compose up --build
and install all neaded modules

2. Документація за допомогою Sphinx
docs/_build/html.

2. Модульні тести за допомогою Unittest
pytest tests/test_repository_contacts.py
or
python -m unittest tests/test_repository_contacts.py

3. Функціональні тести за допомогою Pytest
pip install pytest-asyncio httpx
pytest
