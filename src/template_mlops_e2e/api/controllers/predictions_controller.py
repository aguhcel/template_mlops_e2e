import logging

from fastapi import APIRouter

from src.template_mlops_e2e.api.views.predictions import PredictionsRequest, PredictionsResponse
from src.template_mlops_e2e.pipelines.predict import Predictor

perdictor_router = APIRouter()
logger = logging.getLogger(__name__)

@perdictor_router.get(
    "/test_predict",
    tags=["predictions"],
    status_code=200,
)
def test_predict() -> str:
    predictor = Predictor(config_path="configs/config.yaml")
    predictor.run_test()
    return "Test completed"

@perdictor_router.post(
    "/predict",
    tags=["predictions"],
    status_code=200,
    response_model=PredictionsResponse,
)
def predict(request: PredictionsRequest) -> PredictionsResponse:
    predictor = Predictor(config_path="configs/config.yaml")
    data = request.data
    prediction = predictor.run(data)

    return PredictionsResponse(prediction=prediction)
