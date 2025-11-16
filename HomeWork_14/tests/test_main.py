# tests/test_main.py

import pytest
from fastapi.testclient import TestClient

from main import app
from database.db import get_db

# Ми будемо використовувати цю функцію, щоб замінити get_db з main.py
@pytest.fixture(scope="function")
def override_get_db(session):
    def _override_get_db():
        yield session

    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_read_root(override_get_db):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Contacts API!"}

def test_health_check(override_get_db):
    response = client.get("/api/healthchecker")
    assert response.status_code == 200
    # Correct the expected JSON message
    assert response.json() == {"message": "Database is healthy!"}
# Додайте інші тести для вашого API тут