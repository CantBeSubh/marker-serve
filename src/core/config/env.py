import os
from typing import Optional, Set

from dotenv import load_dotenv

load_dotenv()


class Environment:
    """
    Singleton class for accessing environment variables as attributes.

    Usage:
        from src.core.config import env

        # Access as attributes
        uri = env.mongodb_uri
        port = env.port
    """

    _instance: Optional["Environment"] = None
    _initialized: bool = False
    _accessed_vars: Set[str] = set()

    # Define all environment variables as class variables with default values
    # FastAPI Settings
    api_v1_token: str = os.getenv("API_V1_TOKEN", "")
    port: int = int(os.getenv("PORT", "8080"))
    debug: bool = os.getenv("DEBUG", "").lower() in ("true", "1", "yes", "y", "t")
    allowed_origins: str = os.getenv("ALLOWED_ORIGINS", "*")

    def __new__(cls) -> "Environment":
        if cls._instance is None:
            cls._instance = super(Environment, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._initialized = True


env = Environment()
