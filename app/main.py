import logging
import time
from typing import (
    Callable,
    Dict,
    Final,
    Tuple,
)

from app.application.api.books.handlers import (
    create_book,
    delete_book,
    read_all_books,
    read_book,
    update_book,
)
from app.settings.logger.config import setup_logging


CHOICES_FOR_ACTION: Final[Tuple[str, ...]] = (
    "\n--- Menu of Library ---",
    "1. Add book",
    "2. Delete book",
    "3. Find book",
    "4. Show all books",
    "5. Update book",
    "6. Exit"
)

ACTIONS: Final[Dict[str, Callable[[], None]]] = {
    "1": create_book,
    "2": delete_book,
    "3": read_book,
    "4": read_all_books,
    "5": update_book,
    "6": exit
}

logger = logging.getLogger(__name__)


def main() -> None:
    while True:
        # Делается с той целью, чтобы информация из-под логгера не пересекалась с обычном потоком вывода
        # Может произойти такая ситуация, как представлено ниже
        # Select an action (1-6): [ERROR] 2024-11-27T18:15:52+0300: Bad name format: fedos
        time.sleep(0.2)
        for comment in CHOICES_FOR_ACTION:
            print(comment)

        choice = input("Select an action (1-6): ").strip()

        if choice not in ACTIONS:
            logger.error("Invalid choice! Please select a valid option (1-6).")
            continue

        ACTIONS[choice]()


if __name__ == "__main__":
    setup_logging()
    main()
