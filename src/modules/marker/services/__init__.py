import base64
import logging
import tempfile
from io import BytesIO

from fastapi import UploadFile
from marker.converters.pdf import PdfConverter
from marker.logger import configure_logging
from marker.output import text_from_rendered
from typing_extensions import Annotated

from src.core.config.marker import create_marker_config_parser
from src.core.logging.chalk import Chalk

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


async def parse_pdf(
    file: UploadFile,
    models: Annotated[any, "A list of models to use for parsing"],
    config: Annotated[dict, "The config to use for parsing"] = None,
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
        filename = file.filename
        file_bytes = await file.read()
        chalk.info(f"Entry time for {filename}")
        chalk.info("Parsing PDF file")
        config_parser = create_marker_config_parser(config or {})
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_bytes)
            temp_path = temp_pdf.name
            chalk.info(f"Temp path: {temp_path}")
            converter = PdfConverter(
                artifact_dict=models,
                config=config_parser.generate_config_dict(),
                processor_list=config_parser.get_processors(),
                renderer=config_parser.get_renderer(),
                llm_service=config_parser.get_llm_service(),
            )
            rendered = converter(temp_path)
            markdown_text, _, images = text_from_rendered(rendered)
            metadata = rendered.metadata

            chalk.success(f"Model processes complete time for {filename}")
            return {
                "markdown": markdown_text,
                "metadata": dict(metadata),
                "images": images,
                "status": "ok",
            }
    except Exception as e:
        chalk.error(f"Error processing PDF {file.filename}: {str(e)}")
        return {
            "markdown": "",
            "metadata": {},
            "images": {},
            "status": "error",
            "error": str(e),
        }


def parse_images(images: dict) -> dict:
    """
    Parse a dictionary of image filenames and PIL Image objects.
    Returns a dictionary of image filenames and base64 encoded images.
    """
    chalk.info(f"Parsing images: {len(images.keys())}")
    parsed_images = {}
    for key, img in images.items():
        try:
            img_file = BytesIO()
            img.save(img_file, format="JPEG")
            im_bytes = img_file.getvalue()
            img_b64 = base64.b64encode(im_bytes)
            img_b64_string = img_b64.decode("utf-8")
            parsed_images[key] = img_b64_string
        except Exception as e:
            chalk.warn(f"Error processing image {key}: {str(e)}")
            parsed_images[key] = ""
    chalk.success(f"Parsed images: {len(images.keys())}")
    return parsed_images
