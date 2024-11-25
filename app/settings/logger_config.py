import atexit
import json
import logging
import logging.config
import os
from typing import Final

from app.settings.config import PROJECT_DIR

logger = logging.getLogger(__name__)

PATH_TO_LOGGER_CONFIG: Final[os.PathLike[str]] = PROJECT_DIR / "resources" / "config" / "logger-config.json"


def setup_logging() -> None:
    """
    This function setups the logging configuration.
    Configuration taken from here: https://www.youtube.com/watch?v=9L77QExPmI0
    """
    config_file = PATH_TO_LOGGER_CONFIG
    with open(config_file) as f_in:
        config = json.load(f_in)

    log_dir = PROJECT_DIR / "resources" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    config["handlers"]["file"]["filename"] = str(log_dir / "debug-info.log")

    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore[attr-defined]
        atexit.register(queue_handler.listener.stop)  # type: ignore[attr-defined]