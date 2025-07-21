from typing import Dict, Optional

from pydantic import BaseModel


class ConvertResponse(BaseModel):
    status: str
    filename: str
    markdown: str
    metadata: dict
    images: Dict[str, str]
    error: Optional[str]
    time: float
