from typing import (
    Dict,
    List,
    Type,
    TypeVar,
)

from app.logic.commands.base import AbstractCommand
from app.logic.commands.books import (
    CreateBookCommand,
    DeleteBookCommand,
    GetAllBooksCommand,
    GetBookByIdCommand,
    GetBookByTitleAndAuthorCommand,
    GetBookByTitleCommand,
    UpdateBookCommand,
)
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
    AbstractHandler,
    CT,
    ET,
)
from app.logic.handlers.books.commands import (
    CreateBookCommandHandler,
    DeleteBookCommandHandler,
    GetAllBooksCommandHandler,
    GetBookByIdCommandHandler,
    GetBookByTitleAndAuthorCommandHandler,
    GetBookByTitleCommandHandler,
    UpdateBookCommandHandler,
)


EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[ET], List[Type[AbstractEventHandler[ET]]]] = {}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[CT], Type[AbstractCommandHandler[CT]]] = {
    CreateBookCommand: CreateBookCommandHandler,
    GetBookByIdCommand: GetBookByIdCommandHandler,
    GetBookByTitleCommand: GetBookByTitleCommandHandler,
    GetBookByTitleAndAuthorCommand: GetBookByTitleAndAuthorCommandHandler,
    GetAllBooksCommand: GetAllBooksCommandHandler,
    UpdateBookCommand: UpdateBookCommandHandler,
    DeleteBookCommand: DeleteBookCommandHandler,
}
