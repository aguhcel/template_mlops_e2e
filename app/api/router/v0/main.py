from fastapi import FastAPI, APIRouter

from src.template_mlops_e2e.api.controllers.healthcheck_controller import health_check_router
from src.template_mlops_e2e.api.controllers.predictions_controller import perdictor_router

app = FastAPI(
    title="Template_MLOps_E2E",
    version="0.1.0",
)

api_router = APIRouter()


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root Get
    """
    return {"message": "Hello World!"}


app.include_router(api_router)
app.include_router(health_check_router)
app.include_router(perdictor_router)
