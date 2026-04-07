import pandas as pd
import pandera.pandas as pa
import pytest

from src.template_mlops_e2e.models.validation_schema import iris_schema

VALID_ROW = {
    "SepalLengthCm": [5.1],
    "SepalWidthCm": [3.5],
    "PetalLengthCm": [1.4],
    "PetalWidthCm": [0.2],
    "Species": ["Iris-setosa"],
}


def test_valid_dataframe_passes():
    # Arrange
    df = pd.DataFrame(VALID_ROW)

    # Act & Assert
    iris_schema.validate(df)


def test_null_value_fails():
    # Arrange
    df = pd.DataFrame({**VALID_ROW, "SepalLengthCm": [None]})

    # Act & Assert
    with pytest.raises(pa.errors.SchemaError):
        iris_schema.validate(df)


def test_non_positive_value_fails():
    # Arrange
    df = pd.DataFrame({**VALID_ROW, "PetalWidthCm": [0.0]})

    # Act & Assert
    with pytest.raises(pa.errors.SchemaError):
        iris_schema.validate(df)


def test_invalid_species_fails():
    # Arrange
    df = pd.DataFrame({**VALID_ROW, "Species": ["Iris-unknown"]})

    # Act & Assert
    with pytest.raises(pa.errors.SchemaError):
        iris_schema.validate(df)


def test_missing_column_fails():
    # Arrange
    df = pd.DataFrame(VALID_ROW).drop(columns=["Species"])

    # Act & Assert
    with pytest.raises(pa.errors.SchemaError):
        iris_schema.validate(df)


def test_extra_column_fails():
    # Arrange
    df = pd.DataFrame({**VALID_ROW, "ExtraCol": [99]})

    # Act & Assert
    with pytest.raises(pa.errors.SchemaError):
        iris_schema.validate(df)
