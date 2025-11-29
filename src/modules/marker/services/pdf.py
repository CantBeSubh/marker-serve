import logging
import tempfile
from datetime import datetime

from fastapi import UploadFile
from marker.converters.pdf import PdfConverter
from marker.logger import configure_logging
from marker.output import text_from_rendered
from typing_extensions import Annotated

from src.core.config.marker import create_marker_config_parser
from src.core.logging.chalk import Chalk
from src.modules.marker.services.map_reduce import map_input, reduce_outputs

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


async def parse_pdf_chunk(
    chunk_bytes: bytes,
    chunk_id: str,
    filename: str,
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
        chalk.info(f"Parsing PDF file Chunk {chunk_id}")
        config_parser = create_marker_config_parser(config or {})
        with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
            temp_pdf.write(chunk_bytes)
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

            chalk.success(
                f"Model processes complete time for {filename} | CHUNK {chunk_id}"
            )
            return {
                "chunk_id": chunk_id,
                "markdown": markdown_text,
                "metadata": dict(metadata),
                "images": images,
                "status": "ok",
            }
    except Exception as e:
        chalk.error(f"Error processing PDF {filename} | CHUNK {chunk_id}: {str(e)}")
        return {
            "chunk_id": chunk_id,
            "markdown": "",
            "metadata": {},
            "images": {},
            "status": "error",
            "error": str(e),
        }


async def parse_pdf(
    file: UploadFile,
    models: Annotated[any, "A list of models to use for parsing"],
    config: Annotated[dict, "The config to use for parsing"] = None,
) -> dict:
    filename = file.filename
    chalk.info(f"Entry time for {filename}")
    chunks = await map_input(file=file)
    results = []
    chunk_count = len(chunks)
    for chunk in chunks:
        time = datetime.now()
        result = await parse_pdf_chunk(
            chunk_bytes=chunk,
            chunk_id=f"{len(results):05}",
            filename=filename,
            models=models,
            config=config,
        )
        results.append(result)
        delta = datetime.now() - time
        chunk_parsing_rate = 1 / delta.total_seconds()
        eta = (chunk_count - len(results)) / chunk_parsing_rate
        chalk.info(
            f"Chunk parsing rate for {filename}: {chunk_parsing_rate} chunks/sec"
        )
        chalk.info(f"ETA for {filename}: {eta} seconds")

    return await reduce_outputs(results)
