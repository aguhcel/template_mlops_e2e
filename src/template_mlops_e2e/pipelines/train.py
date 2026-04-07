from pathlib import Path
from typing import Tuple

import pandas as pd
from joblib import dump
from yaml import safe_load

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class Trainer:
    config_path: str | Path 

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = config_path
        self.config = self._load_config(self.config_path)

    def _load_config(self, path: str | Path) -> dict:
        with open(path, "r", encoding="utf-8") as file:
            return safe_load(file)
        
    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.config["data"]["silver_path"])

    def split_data(self, data: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        train, test = train_test_split(
            data, 
            test_size=self.config["model"]["test_size"],
            random_state=self.config["model"]["random_state"]
        )

        return train, test
    
    def train_model(self, train_X: pd.DataFrame, train_y: pd.Series) -> LogisticRegression:
        model = LogisticRegression(random_state=self.config["model"]["random_state"])
        model.fit(train_X, train_y)

        return model
    
    def save_data(self, data: pd.DataFrame, path_key: str) -> None:
        data.to_csv(self.config["data"][path_key], index=False)
    
    def save_model(self, model: LogisticRegression) -> None:
        dump(model, self.config["model"]["output_path"])
    
    def run(self) -> None:
        data = self.load_data()

        train, test = self.split_data(data)

        self.save_data(train, "train_path")
        self.save_data(test, "test_path")

        train_X = train.drop(columns=[self.config["model"]["target"]])
        train_y = train[self.config["model"]["target"]]

        model = self.train_model(train_X, train_y)

        self.save_model(model)
