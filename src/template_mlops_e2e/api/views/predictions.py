from pydantic import BaseModel

class UserData(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

class PredictionsRequest(BaseModel):
    data: UserData

class PredictionsResponse(BaseModel):
    prediction: str