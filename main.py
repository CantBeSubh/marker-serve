import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from marker.logger import configure_logging
from marker.models import create_model_dict

from src.api.v1.core import v1_router
from src.core.config.env import env
from src.core.logging import Chalk

configure_logging()
logger = logging.getLogger(__name__)

models = None
chalk = Chalk()


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    global models
    try:
        chalk.info("Loading models...")
        models = create_model_dict()
        yield
        chalk.warn("Server shutting down...")
    except Exception as e:
        chalk.error(f"Error loading models: {str(e)}")
        raise


app = FastAPI(lifespan=lifespan, title="Marker Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[env.allowed_origins],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/health")
async def health() -> dict:
    return {"message": "OK"}


app.include_router(v1_router)
