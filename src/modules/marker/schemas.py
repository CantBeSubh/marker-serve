from typing import Optional

from pydantic import BaseModel


class ConvertResponse(BaseModel):
    status: str
    markdown: str
    metadata: dict
    # images: dict  # TODO: Getting class mismatch error (PIL)
    error: Optional[str] = None  # Set a default value of None
