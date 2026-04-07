from unittest.mock import MagicMock, patch, mock_open

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.template_mlops_e2e.api.controllers.predictions_controller import perdictor_router

app = FastAPI()
app.include_router(perdictor_router)
client = TestClient(app)

VALID_PAYLOAD = {
    "data": {
        "SepalLengthCm": 5.1,
        "SepalWidthCm": 3.5,
        "PetalLengthCm": 1.4,
        "PetalWidthCm": 0.2,
    }
}

@patch("src.template_mlops_e2e.api.controllers.predictions_controller.Predictor")
def test_test_predict_returns_200(mock_predictor_class):
    # Arrange
    mock_predictor_class.return_value.run_test = MagicMock()

    # Act
    response = client.get("/test_predict")

    # Assert
    assert response.status_code == 200


@patch("src.template_mlops_e2e.api.controllers.predictions_controller.Predictor")
def test_test_predict_returns_completed_message(mock_predictor_class):
    # Arrange
    mock_predictor_class.return_value.run_test = MagicMock()

    # Act
    response = client.get("/test_predict")

    # Assert
    assert response.json() == "Test completed"


@patch("src.template_mlops_e2e.api.controllers.predictions_controller.Predictor")
def test_predict_returns_200(mock_predictor_class):
    # Arrange
    mock_predictor_class.return_value.run.return_value = "Iris-setosa"

    # Act
    response = client.post("/predict", json=VALID_PAYLOAD)

    # Assert
    assert response.status_code == 200


@patch("src.template_mlops_e2e.api.controllers.predictions_controller.Predictor")
def test_predict_returns_prediction(mock_predictor_class):
    # Arrange
    mock_predictor_class.return_value.run.return_value = "Iris-setosa"

    # Act
    response = client.post("/predict", json=VALID_PAYLOAD)

    # Assert
    assert response.json() == {"prediction": "Iris-setosa"}


@patch("src.template_mlops_e2e.api.controllers.predictions_controller.Predictor")
def test_predict_calls_run_with_correct_data(mock_predictor_class):
    # Arrange
    mock_run = MagicMock(return_value="Iris-virginica")
    mock_predictor_class.return_value.run = mock_run

    # Act
    client.post("/predict", json=VALID_PAYLOAD)

    # Assert
    mock_run.assert_called_once()


def test_predict_missing_field_returns_422():
    # Arrange
    incomplete_payload = {"data": {"SepalLengthCm": 5.1}}

    # Act
    response = client.post("/predict", json=incomplete_payload)

    # Assert
    assert response.status_code == 422
    