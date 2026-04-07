from unittest.mock import MagicMock, mock_open, patch, call

import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression

from src.template_mlops_e2e.pipelines.train import Trainer

CONFIG = {
    "data": {
        "silver_path": "data/silver/Iris_clean.csv",
        "train_path": "data/gold/Iris_train.csv",
        "test_path": "data/gold/Iris_test.csv",
    },
    "model": {
        "target": "Species",
        "test_size": 0.3,
        "random_state": 42,
        "output_path": "models/iris_model.pkl",
    },
}

SAMPLE_DF = pd.DataFrame({
    "SepalLengthCm": [5.1, 6.2, 4.9, 5.8, 6.0],
    "SepalWidthCm":  [3.5, 2.9, 3.1, 2.7, 3.0],
    "PetalLengthCm": [1.4, 4.3, 1.5, 5.1, 4.8],
    "PetalWidthCm":  [0.2, 1.3, 0.2, 1.9, 1.8],
    "Species": ["Iris-setosa", "Iris-versicolor", "Iris-setosa", "Iris-virginica", "Iris-virginica"],
})


@pytest.fixture
def trainer():
    with patch.object(Trainer, "_load_config", return_value=CONFIG):
        return Trainer(config_path="configs/config.yaml")

def test_load_config_parses_yaml(trainer):
    # Arrange
    yaml_content = "model:\n  target: Species\n"

    # Act
    with patch("builtins.open", mock_open(read_data=yaml_content)):
        result = trainer._load_config("any/path.yaml")

    # Assert
    assert result == {"model": {"target": "Species"}}


def test_load_data_returns_dataframe(trainer):
    # Arrange & Act
    with patch("pandas.read_csv", return_value=SAMPLE_DF.copy()) as mock_csv:
        result = trainer.load_data()

    # Assert
    mock_csv.assert_called_once_with(CONFIG["data"]["silver_path"])
    assert isinstance(result, pd.DataFrame)


def test_split_data_returns_correct_proportions(trainer):
    # Arrange
    df = SAMPLE_DF.copy()

    # Act
    train, test = trainer.split_data(df)

    # Assert
    assert len(train) + len(test) == len(df)
    assert len(test) == pytest.approx(len(df) * 0.3, abs=1)


def test_train_model_returns_fitted_logistic_regression(trainer):
    # Arrange
    train_X = SAMPLE_DF.drop(columns=["Species"])
    train_y = SAMPLE_DF["Species"]

    # Act
    model = trainer.train_model(train_X, train_y)

    # Assert
    assert isinstance(model, LogisticRegression)
    assert hasattr(model, "classes_")  # indica que está entrenado


def test_save_data_writes_to_correct_path(trainer):
    # Arrange
    mock_to_csv = MagicMock()
    df = SAMPLE_DF.copy()
    df.to_csv = mock_to_csv

    # Act
    trainer.save_data(df, "train_path")

    # Assert
    mock_to_csv.assert_called_once_with(CONFIG["data"]["train_path"], index=False)


def test_save_model_calls_joblib_dump(trainer):
    # Arrange
    mock_model = MagicMock()

    # Act
    with patch("src.template_mlops_e2e.pipelines.train.dump") as mock_dump:
        trainer.save_model(mock_model)

    # Assert
    mock_dump.assert_called_once_with(mock_model, CONFIG["model"]["output_path"])


def test_run_orchestrates_all_steps(trainer):
    # Arrange
    mock_model = MagicMock()

    # Act
    with patch.object(trainer, "load_data", return_value=SAMPLE_DF.copy()), \
         patch.object(trainer, "save_data") as mock_save_data, \
         patch.object(trainer, "train_model", return_value=mock_model), \
         patch.object(trainer, "save_model") as mock_save_model:
        trainer.run()

    # Assert
    assert mock_save_data.call_count == 2  # train y test
    mock_save_model.assert_called_once_with(mock_model)
