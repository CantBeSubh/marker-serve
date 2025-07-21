import base64
import logging
import os
import time

from fastapi import UploadFile
from marker.convert import convert_single_pdf
from marker.logger import configure_logging

from src.core.logging import Chalk

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


async def parse_pdf(file: UploadFile, model_list, extract_images=True) -> dict:
    """
    Parse a PDF file using the provided model list.
    Returns a dictionary with the following keys:

    Arguments:
    - file: The PDF file to parse
    - model_list: A list of models to use for parsing
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
        logger.info(chalk.blue(f"Entry time for {filename}: {entry_time}"))
        logger.debug(chalk.blue("Parsing PDF file"))
        markdown_text, images, metadata = await convert_single_pdf(
            file_bytes, model_list
        )
        logger.debug(chalk.blue(f"Images extracted: {list(images.keys())}"))
        image_data = {}
        if extract_images:
            for i, (filename, image) in enumerate(images.items()):
                logger.debug(chalk.blue(f"Processing image {filename}"))

                image.save(filename, "PNG")
                with open(filename, "rb") as f:
                    image_bytes = f.read()
                image_base64 = base64.b64encode(image_bytes).decode("utf-8")
                image_data[f"{filename}"] = image_base64
                os.remove(filename)

        completion_time = time.time()
        logger.info(
            chalk.green(
                f"Model processes complete time for {filename}: {completion_time}"
            )
        )
        time_difference = completion_time - entry_time
        return {
            "filename": filename,
            "markdown": markdown_text,
            "metadata": metadata,
            "images": image_data,
            "status": "ok",
            "time": time_difference,
        }
    except Exception as e:
        logger.error(chalk.red(f"Error processing PDF {file.filename}: {str(e)}"))
        return {
            "filename": file.filename,
            "markdown": "",
            "metadata": {},
            "images": {},
            "status": "error",
            "error": str(e),
            "time": 0,
        }
