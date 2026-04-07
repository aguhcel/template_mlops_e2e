import logging

from fastapi import APIRouter

from src.template_mlops_e2e.api.views.healthcheck import HealthCheckResponse

health_check_router = APIRouter()
logger = logging.getLogger(__name__)


@health_check_router.get(
    "/health",
    tags=["health"],
    status_code=200,
    responses={200: {"status": "ok"}},
)
def health_check() -> HealthCheckResponse:
    return HealthCheckResponse(status="ok")
