from typing import List, Dict, Type

from app.logic.commands.base import AbstractCommand
from app.logic.commands.books import (
    CreateBookCommand,
    UpdateBookCommand,
    DeleteBookCommand,
    GetBookByIdCommand,
    GetBookByTitleCommand,
    GetAllBooksCommand
)
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import AbstractEventHandler, AbstractCommandHandler
from app.logic.handlers.books.commands import (
    CreateBookCommandHandler,
    UpdateBookCommandHandler,
    DeleteBookCommandHandler,
    GetBookByIdCommandHandler,
    GetBookByTitleCommandHandler,
    GetAllBooksCommandHandler
)

EVENTS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractEvent], List[Type[AbstractEventHandler]]] = {

}

COMMANDS_HANDLERS_FOR_INJECTION: Dict[Type[AbstractCommand], Type[AbstractCommandHandler]] = {
    CreateBookCommand: CreateBookCommandHandler,
    GetBookByIdCommand: GetBookByIdCommandHandler,
    GetBookByTitleCommand: GetBookByTitleCommandHandler,
    GetAllBooksCommand: GetAllBooksCommandHandler,
    UpdateBookCommand: UpdateBookCommandHandler,
    DeleteBookCommand: DeleteBookCommandHandler,
}
