from typing import Final, Tuple, Dict, Callable

from app.application.api.books.handlers import (
    create,
    delete,
    update,
    read,
    read_all
)

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
    "1": create,
    "2": delete,
    "3": read,
    "4": read_all,
    "5": update,
    "6": exit
}


def main() -> None:
    while True:
        for comment in CHOICES_FOR_ACTION:
            print(comment)

        choice = input("Select an action (1-6): ").strip()

        if choice not in ACTIONS:
            print("Invalid choice! Please select a valid option (1-6).")
            continue

        ACTIONS[choice]()


if __name__ == "__main__":
    main()
