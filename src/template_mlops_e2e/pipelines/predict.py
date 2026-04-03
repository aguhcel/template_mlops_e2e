from pathlib import Path
from typing import Any

import pandas as pd
from joblib import load
from yaml import safe_load

from app.api.router.predictions.models.prediction_model import UserData

class Predictor:
    config_path: str | Path

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = config_path
        self.config = self._load_config(self.config_path)

    def _load_config(self, path: str | Path) -> dict:
        with open(path, "r", encoding="utf-8") as file:
            return safe_load(file)
        
    def load_data(self, path: str | Path) -> pd.DataFrame:
        return pd.read_csv(path)

    def load_model(self) -> Any:
        return load(self.config["model"]["output_path"])

    def _get_features(self, data: pd.DataFrame) -> pd.DataFrame:
        target = self.config["model"]["target"]
        if target in data.columns:
            return data.drop(columns=[target])
        return data

    def predict(self, model: Any, data: pd.DataFrame) -> pd.Series:
        features = self._get_features(data)
        return pd.Series(model.predict(features))

    def run_test(self) -> None:
        model = self.load_model()
        data_test = self.load_data(self.config["data"]["test_path"])
        predictions = self.predict(model, data_test)

        target = self.config["model"]["target"]
        equal = predictions == data_test[target]
        if equal.all(): 
            print("All predictions are correct!")
        else:
            not_equal = data_test[~equal]
            print(f"Some predictions are incorrect. Incorrect predictions:\n{not_equal}")

    
    def run(self, data: UserData) -> str:
        input_data = pd.DataFrame(data.model_dump(), index=[0])

        model = self.load_model()

        return model.predict(input_data)[0]
