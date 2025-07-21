import logging

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from typing_extensions import Annotated

from src.core.logging import Chalk

from .schemas import ConvertResponse
from .services import parse_pdf

logger = logging.getLogger(__name__)

chalk = Chalk()


router = APIRouter(tags=["Chat"])


def get_model_list() -> any:
    from main import model_list

    if model_list is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    return model_list


@router.post("/convert", response_model=ConvertResponse)
async def convert(
    pdf_file: UploadFile,
    models: Annotated[any, "List of models to use for parsing"] = Depends(
        get_model_list
    ),
) -> ConvertResponse:
    try:
        logger.info(chalk.blue(f"Converting PDF: {pdf_file.filename}"))
        result = await parse_pdf(pdf_file, models)
        logger.info(chalk.green(f"PDF converted: {pdf_file.filename}"))
        return ConvertResponse(status="ok", **result)
    except Exception as e:
        logger.error(chalk.red(f"Error converting PDF {pdf_file.filename}: {str(e)}"))
        raise HTTPException(status_code=500, detail=str(e))
