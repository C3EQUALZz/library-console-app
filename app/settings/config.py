import atexit
import json
import logging
import logging.config
import logging.handlers
import pathlib
from dataclasses import dataclass
from typing import Final

logger = logging.getLogger(__name__)

PROJECT_DIR: Final[pathlib.Path] = pathlib.Path(__file__).parent.parent.parent


@dataclass(frozen=True)
class LoggerSettings:
    """
    The configuration was taken from video: https://youtu.be/9L77QExPmI0?si=ZB9GTB08OY7cMhyR
    """
    __path_to_logger_config = PROJECT_DIR / "resources" / "config" / "logger-config.json"

    def __post_init__(self) -> None:
        config_file = self.__path_to_logger_config
        with open(config_file) as f_in:
            config = json.load(f_in)

        log_dir = PROJECT_DIR / "resources" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Почему-то работает только, если прописывать абсолютный путь до файла
        # Разными способами пытался в json конфигурацию сделать, но бесполезно
        config['handlers']['file']['filename'] = str(log_dir / "debug-info.log")

        logging.config.dictConfig(config)
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is not None:
            queue_handler.listener.start() # type: ignore[attr-defined]
            atexit.register(queue_handler.listener.stop) # type: ignore[attr-defined]


@dataclass(frozen=True)
class Settings:
    path_to_database_json_file: pathlib.Path = PROJECT_DIR / "resources" / "data" / "database.json"
    logger_settings: LoggerSettings = LoggerSettings()

    def __post_init__(self) -> None:
        self.path_to_database_json_file.parent.mkdir(parents=True, exist_ok=True)


settings = Settings()
