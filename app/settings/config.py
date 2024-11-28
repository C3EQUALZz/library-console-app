import logging.handlers
import pathlib
from dataclasses import dataclass
from typing import Final


logger = logging.getLogger(__name__)

PROJECT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent.parent.parent


@dataclass(frozen=True)
class Settings:
    """
    In real cases this class must be pydantic BaseModel which contains all urls to connect database, redis and etc.
    """
    path_to_database_json_file: pathlib.Path = PROJECT_DIR / "resources" / "data" / "database.json"

    def __post_init__(self) -> None:
        self.path_to_database_json_file.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
