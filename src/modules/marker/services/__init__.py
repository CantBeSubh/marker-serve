import base64
import logging
import os
import tempfile
import time

from fastapi import UploadFile
from marker.converters.pdf import PdfConverter
from marker.logger import configure_logging
from marker.output import text_from_rendered
from typing_extensions import Annotated

from src.core.logging import Chalk

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


async def parse_pdf(
    file: UploadFile,
    models: Annotated[any, "A list of models to use for parsing"],
    extract_images: Annotated[bool, "Whether to extract images from the PDF"] = True,
) -> dict:
    """
    Parse a PDF file using the provided model list.
    Returns a dictionary with the following keys:

    Arguments:
    - file: The PDF file to parse
    - models: A list of models to use for parsing
    - extract_images: Whether to extract images from the PDF

    Returns:
    - filename: The original filename of the PDF
    - markdown: The extracted Markdown text
    - metadata: The extracted metadata
    - images: A dictionary of image filenames and base64 encoded images
    - status: Either "ok" or "error"
    - error: If status is "error", this will contain the error message
    - time: The time taken to process the PDF
    """
    try:
        entry_time = time.time()
        filename = file.filename
        file_bytes = await file.read()
        print(chalk.blue(f"Entry time for {filename}: {entry_time}"))
        print(chalk.blue("Parsing PDF file"))
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_path = temp_pdf.name
            print(chalk.blue(f"Temp path: {temp_path}"))
            converter = PdfConverter(artifact_dict=models)
            rendered = converter(temp_path)
            markdown_text, _, images = text_from_rendered(rendered)
            metadata = rendered.metadata
            completion_time = time.time()

            print(
                chalk.green(
                    f"Model processes complete time for {filename}: {completion_time}"
                )
            )
            return {
                "markdown": markdown_text,
                "metadata": dict(metadata),
                "images": dict(images),
                "status": "ok",
            }
    except Exception as e:
        print(chalk.red(f"Error processing PDF {file.filename}: {str(e)}"))
        return {
            "markdown": "",
            "metadata": {},
            "images": {},
            "status": "error",
            "error": str(e),
        }
