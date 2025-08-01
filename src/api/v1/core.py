from fastapi import APIRouter, Depends

from src.api.v1.auth import verify_token
from src.core.config.env import env
from src.modules.marker.routers import router as marker_router

disable_auth = env.disable_auth == "True"

if disable_auth:
    v1_router = APIRouter(
        prefix="/v1",
        tags=["v1"],
    )

else:
    v1_router = APIRouter(
        prefix="/v1",
        tags=["v1"],
        dependencies=[Depends(verify_token)],
    )

v1_router.include_router(marker_router)
