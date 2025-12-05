import logging
import re
from io import BytesIO

from fastapi import HTTPException, UploadFile
from marker.logger import configure_logging
from PyPDF2 import PdfReader, PdfWriter

from src.core.logging.chalk import Chalk

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


async def map_input(file: UploadFile) -> list[bytes]:
    """
    Map an input file to a list of bytes.
    Returns a list of bytes.
    FOR MVP - Each Chunk is each page
    """
    try:
        file_bytes = await file.read()
        chalk.info("Chunking PDF file")
        chunks = []

        with BytesIO(file_bytes) as pdf_stream:
            reader = PdfReader(pdf_stream)
            num_pages = len(reader.pages)

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                writer_stream = BytesIO()
                writer = PdfWriter()
                writer.add_page(page)
                writer.write(writer_stream)
                chunks.append(writer_stream.getvalue())
                writer_stream.close()

        chalk.success(f"Chunked PDF file by page: {len(chunks)} chunks")
        return chunks
    except Exception as e:
        chalk.error(f"Error mapping input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def slide_output(output: dict) -> dict:
    """
    Slide the output's page number by the chunk_id.
    This is used to adjust the page numbers in the output. For example, if the
    chunk_id is 1, then the page number in the output will be incremented by 1.
    """
    chunk_id = int(output["chunk_id"])
    chalk.info(f"Adjusting chunk_id={chunk_id}")

    md = ""
    metadata = {}
    if output["metadata"]:
        metadata = output["metadata"]
        if metadata["table_of_contents"]:
            tocs = metadata["table_of_contents"]
            for toc in tocs:
                toc["page_id"] += chunk_id
        if metadata["page_stats"]:
            page_stats = metadata["page_stats"]
            for page_stat in page_stats:
                page_stat["page_id"] += chunk_id

    images = {}
    if output["images"]:
        old_images = output["images"]
        for key, val in old_images.items():
            key_page_id = re.search(r"_page_(\d+)_", key)
            if key_page_id:
                page_id = int(key_page_id.group(1))
                old_key = key.replace(key_page_id.group(0), "")
                new_key = f"_page_{page_id + chunk_id}_{old_key}"
                images[new_key] = val

    md = output["markdown"]

    if md:
        matches = list(re.finditer(r"{(\d+)}-{48}", md))
        for match in matches:
            page_no = match.group(1)
            new_str = f"{{{chunk_id + int(page_no)}}}" + "-" * 48
            old_str = match.group(0)
            md = md.replace(old_str, new_str, 1)
        matches = list(re.finditer(r"_page_(\d+)_", md))
        for match in matches:
            page_no = match.group(1)
            new_str = f"_page_{chunk_id + int(page_no)}_"
            old_str = match.group(0)
            md = md.replace(old_str, new_str, 1)

    return {
        "combined_markdown": md,
        "images": images,
        "metadata": metadata,
    }


async def reduce_outputs(outputs: list[dict]) -> dict:
    """
    Reduce the outputs by combining the markdown, images, and metadata.
    """
    try:
        chalk.info("Reducing output")
        combined_markdown = ""
        images = {}
        metadata = {}

        import asyncio

        tasks = [slide_output(output=output) for output in outputs]
        results = await asyncio.gather(*tasks)
        if results:
            for result in results:
                combined_markdown += result["combined_markdown"]
                for key, val in result["images"].items():
                    images[key] = val
                for key, val in result["metadata"].items():
                    if isinstance(val, list):
                        if key not in metadata:
                            metadata[key] = []
                        metadata[key].extend(val)
                    else:
                        metadata[key] = val
        else:
            raise HTTPException(
                status_code=500, detail="REDUCE ASYNCIO ERROR - empty results"
            )

        chalk.success("Reduced output")

        return {
            "markdown": combined_markdown,
            "metadata": metadata,
            "images": images,
            "status": "ok",
        }
    except Exception as e:
        chalk.error(f"Error reducing output: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
