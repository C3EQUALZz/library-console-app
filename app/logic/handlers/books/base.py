from abc import ABC

from app.infrastructure.uow.books.base import BooksUnitOfWork
from app.logic.handlers.base import (
    AbstractCommandHandler,
    AbstractEventHandler,
    CT,
    ET
)


class BooksEventHandler(AbstractEventHandler[ET], ABC):
    """
    Abstract event handler class, from which every users event handler should be inherited from.
    """

    def __init__(self, uow: BooksUnitOfWork) -> None:
        self._uow: BooksUnitOfWork = uow


class BooksCommandHandler(AbstractCommandHandler[CT], ABC):
    """
    Abstract command handler class, from which every users command handler should be inherited from.
    """

    def __init__(self, uow: BooksUnitOfWork) -> None:
        self._uow: BooksUnitOfWork = uow
