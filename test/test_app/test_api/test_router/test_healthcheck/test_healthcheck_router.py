from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.router.healthcheck.healthcheck_router import health_check_router

app = FastAPI()
app.include_router(health_check_router)
client = TestClient(app)


def test_health_check_returns_200():
    # Arrange / Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200


def test_health_check_returns_ok_status():
    # Arrange / Act
    response = client.get("/health")

    # Assert
    assert response.json() == {"status": "ok"}