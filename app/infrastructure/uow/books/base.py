from abc import ABC

from app.infrastructure.repositories.books.base import BooksRepository
from app.infrastructure.uow.base import AbstractUnitOfWork


class BooksUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with books, that is used by service layer of books module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """

    books: BooksRepository
