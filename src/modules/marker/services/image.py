import base64
import logging
from io import BytesIO

from marker.logger import configure_logging

from src.core.logging.chalk import Chalk

configure_logging()
logger = logging.getLogger(__name__)
chalk = Chalk()


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
