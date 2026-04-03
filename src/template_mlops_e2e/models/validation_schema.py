import yaml
import pandera.pandas as pa

config = yaml.safe_load(open("configs/config.yaml", "r"))

iris_schema = pa.DataFrameSchema({
    "SepalLengthCm": pa.Column(float, nullable=False, checks=pa.Check.gt(0)),
    "SepalWidthCm": pa.Column(float, nullable=False, checks=pa.Check.gt(0)),
    "PetalLengthCm": pa.Column(float, nullable=False, checks=pa.Check.gt(0)),
    "PetalWidthCm": pa.Column(float, nullable=False, checks=pa.Check.gt(0)),
    "Species": pa.Column(str, nullable=False, checks=pa.Check.isin(["Iris-setosa", "Iris-versicolor", "Iris-virginica"]))
    },
    strict=True
)