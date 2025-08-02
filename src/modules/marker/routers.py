import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile,Request
from typing_extensions import Annotated

from src.core.logging.chalk import Chalk

from .schemas import ConvertResponse
from .services import parse_pdf

logger = logging.getLogger(__name__)

chalk = Chalk()


router = APIRouter(tags=["Chat"])


def get_models() -> any:
    from main import models

    if models is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return models


@router.post("/convert", response_model=ConvertResponse)
async def convert(
    request:Request,
    file: UploadFile,
    models: Annotated[any, "List of models to use for parsing"] = Depends(get_models),
) -> ConvertResponse:
    try:
        form_data = await request.form()
        config = dict(form_data)
        chalk.info(f"Converting PDF: {file.filename}")
        del config["file"]
        chalk.info(f"Config Params: {config.keys()}")
        chalk.info(f"Config Values: {config}")
        result = await parse_pdf(file, models, config=config)
        chalk.success(f"PDF converted: {file.filename}")
        return ConvertResponse(**result)
    except Exception as e:
        chalk.error(f"Error converting PDF {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
