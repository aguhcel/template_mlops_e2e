from fastapi.testclient import TestClient

from app.api.router.v0.main import app

client = TestClient(app)


def test_root_returns_200():
    # Arrange / Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200


def test_root_returns_hello_world():
    # Arrange / Act
    response = client.get("/")

    # Assert
    assert response.json() == {"message": "Hello World!"}


def test_health_returns_200():
    # Arrange / Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200


def test_health_returns_ok_status():
    # Arrange / Act
    response = client.get("/health")

    # Assert
    assert response.json() == {"status": "ok"}
