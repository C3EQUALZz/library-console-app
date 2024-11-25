import logging

from typing import Final, Tuple, Dict, Callable

from app.application.api.books.handlers import (
    create_book,
    delete_book,
    update_book,
    read_book,
    read_all_books
)

from app.settings.logger_config import setup_logging

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
        for comment in CHOICES_FOR_ACTION:
            logger.info(comment)

        choice = input("Select an action (1-6): ").strip()

        if choice not in ACTIONS:
            logger.error("Invalid choice! Please select a valid option (1-6).")
            continue

        ACTIONS[choice]()


if __name__ == "__main__":
    setup_logging()
    main()
