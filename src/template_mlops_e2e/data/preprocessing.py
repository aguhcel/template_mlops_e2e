from pathlib import Path
from typing import Iterable

import pandas as pd
import pandera as pa
from yaml import safe_load

from src.template_mlops_e2e.models.validation_schema import iris_schema

class Preprocessor:
    config_path: str | Path

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = config_path
        self.config = self._load_config(self.config_path)

    def _load_config(self, path: str | Path) -> dict:
        with open(path, "r", encoding="utf-8") as file:
            return safe_load(file)

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.config["data"]["bronze_path"])
        
    def fill_nulls(self, data: pd.DataFrame) -> pd.DataFrame:
        if data.isnull().sum().sum() == 0:
            return data
        means = data.mean(numeric_only=True)
        return data.fillna(means)

    def delete_nulls(self, data: pd.DataFrame) -> pd.DataFrame:
        if data.isnull().sum().sum() == 0:
            return data
        return data.dropna()

    def delete_duplicates(self, data: pd.DataFrame) -> pd.DataFrame:
        if data.duplicated().sum() == 0:
            return data
        return data.drop_duplicates()

    def drop_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        cols: Iterable[str] = self.config["data"].get("drop_columns", [])
        return data.drop(columns=list(cols))
    
    def select_features(self, data: pd.DataFrame) -> pd.DataFrame:
        features: Iterable[str] = self.config["data"]["selected_features"]
        return data[list(features)]
    
    def validate(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            return iris_schema.validate(data, lazy=True)
        except (pa.errors.SchemaError, pa.errors.SchemaErrors) as exc:
            print(f"Data validation failed: {exc}")
            raise ValueError(f"Data validation failed: {exc}") from exc

    def save(self, data: pd.DataFrame) -> None:
        data.to_csv(self.config["data"]["silver_path"], index=False)


    def run(self) -> None:
        data = self.extract()
        data = self.fill_nulls(data)
        data = self.delete_nulls(data)
        data = self.delete_duplicates(data)
        data = self.drop_columns(data)
        data = self.select_features(data)

        self.validate(data)
        self.save(data)