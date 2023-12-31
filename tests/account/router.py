import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_login_success():
    # Prepare test data
    login_data = {"username": "testuser", "password": "testpassword"}

    # Make POST request to /login endpoint
    response = client.post("/login", json=login_data)

    # Assert the response status code is 200 OK
    assert response.status_code == 200

    # Assert the response contains expected keys and data
    assert "data" in response.json()
    assert "access_token" in response.json()["data"]
    assert "refresh_token" in response.json()["data"]


def test_login_invalid_credentials():
    # Prepare test data with invalid credentials
    login_data = {"username": "testuser", "password": "invalidpassword"}

    # Make POST request to /login endpoint
    response = client.post("/login", json=login_data)

    # Assert the response status code is 401 Unauthorized or another appropriate error status code
    assert response.status_code == 401
    assert "error_message" in response.json()
    assert response.json()["error_message"] == "Invalid credentials"

