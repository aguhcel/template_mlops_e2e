from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.template_mlops_e2e.pipelines.predict import Predictor

CONFIG = {
    "data": {"test_path": "data/gold/Iris_test.csv"},
    "model": {"output_path": "models/iris_model.pkl", "target": "Species"},
}

SAMPLE_DF = pd.DataFrame({
    "SepalLengthCm": [5.1],
    "SepalWidthCm": [3.5],
    "PetalLengthCm": [1.4],
    "PetalWidthCm": [0.2],
    "Species": ["Iris-setosa"],
})


@pytest.fixture
def predictor():
    with patch.object(Predictor, "_load_config", return_value=CONFIG):
        return Predictor(config_path="configs/config.yaml")
    

def test_load_config_parses_yaml_file(predictor):
    # Arrange
    yaml_content = "model:\n  target: Species\n"

    # Act
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        result = predictor._load_config("any/path.yaml")

    # Assert
    assert result == {"model": {"target": "Species"}}


def test_load_model_calls_joblib_load(predictor):
    # Arrange
    mock_model = MagicMock()

    # Act
    with patch("src.template_mlops_e2e.pipelines.predict.load", return_value=mock_model) as mock_load:
        result = predictor.load_model()

    # Assert
    mock_load.assert_called_once_with(CONFIG["model"]["output_path"])
    assert result is mock_model


def test_load_data_returns_dataframe(predictor):
    # Arrange
    mock_df = SAMPLE_DF.copy()

    # Act
    with patch("pandas.read_csv", return_value=mock_df):
        result = predictor.load_data("fake/path.csv")

    # Assert
    assert isinstance(result, pd.DataFrame)


def test_get_features_drops_target_column(predictor):
    # Arrange
    df = SAMPLE_DF.copy()

    # Act
    result = predictor._get_features(df)

    # Assert
    assert "Species" not in result.columns


def test_get_features_keeps_all_columns_when_no_target(predictor):
    # Arrange
    df = SAMPLE_DF.drop(columns=["Species"])

    # Act
    result = predictor._get_features(df)

    # Assert
    assert list(result.columns) == list(df.columns)


def test_predict_returns_series(predictor):
    # Arrange
    mock_model = MagicMock()
    mock_model.predict.return_value = ["Iris-setosa"]

    # Act
    result = predictor.predict(mock_model, SAMPLE_DF.copy())

    # Assert
    assert isinstance(result, pd.Series)


def test_run_returns_prediction_string(predictor):
    # Arrange
    mock_user_data = MagicMock()
    mock_user_data.model_dump.return_value = {
        "SepalLengthCm": 5.1,
        "SepalWidthCm": 3.5,
        "PetalLengthCm": 1.4,
        "PetalWidthCm": 0.2,
    }
    mock_model = MagicMock()
    mock_model.predict.return_value = ["Iris-setosa"]

    # Act
    with patch.object(predictor, "load_model", return_value=mock_model):
        result = predictor.run(mock_user_data)

    # Assert
    assert result == "Iris-setosa"


def test_run_test_prints_correct_when_all_match(predictor, capsys):
    # Arrange
    mock_model = MagicMock()
    mock_model.predict.return_value = ["Iris-setosa"]

    # Act
    with patch.object(predictor, "load_model", return_value=mock_model), \
         patch.object(predictor, "load_data", return_value=SAMPLE_DF.copy()):
        predictor.run_test()

    # Assert
    captured = capsys.readouterr()
    assert "All predictions are correct!" in captured.out


def test_run_test_prints_incorrect_when_mismatch(predictor, capsys):
    # Arrange
    df = SAMPLE_DF.copy()
    mock_model = MagicMock()
    mock_model.predict.return_value = ["Iris-virginica"]  # distinto a "Iris-setosa"

    # Act
    with patch.object(predictor, "load_model", return_value=mock_model), \
         patch.object(predictor, "load_data", return_value=df):
        predictor.run_test()

    # Assert
    captured = capsys.readouterr()
    assert "Some predictions are incorrect" in captured.out