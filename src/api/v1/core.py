from fastapi import APIRouter, Depends

from src.api.v1.auth import verify_token
from src.modules.marker.routers import router as marker_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
    dependencies=[Depends(verify_token)],
)

v1_router.include_router(marker_router)
