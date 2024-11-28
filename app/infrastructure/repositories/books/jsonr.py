from abc import ABC
from typing import (
    List,
    Optional,
    override,
)

from app.domain.entities.books import Book
from app.infrastructure.exceptions import BookNotFoundException
from app.infrastructure.repositories.base import (
    AbstractRepository,
    BaseEntityType,
)
from app.infrastructure.repositories.books.base import BooksRepository


class JsonAbstractRepository(AbstractRepository[BaseEntityType], ABC):
    """
    Repository interface for json, from which should be inherited all other repositories.
    """

    def __init__(self, session: List[BaseEntityType]) -> None:
        self._session = session


class JsonBooksRepository(JsonAbstractRepository[Book], BooksRepository):
    @override
    def __init__(self, session: List[Book]) -> None:
        super().__init__(session)

    @override
    def get_by_title(self, title: str) -> Optional[Book]:
        return next((book for book in self._session if book.title.as_generic_type() == title), None)

    @override
    def get_by_title_and_author(self, title: str, author: str) -> Optional[Book]:
        return next((book for book in self._session if
                     book.title.as_generic_type() == title
                     and
                     book.author.as_generic_type() == author), None)

    @override
    def add(self, model: Book) -> Book:
        self._session.append(model)
        return model

    @override
    def get(self, oid: str) -> Optional[Book]:
        return next((book for book in self._session if book.oid == oid), None)

    @override
    def update(self, oid: str, model: Book) -> Book:
        for idx, book in enumerate(self._session):
            if book.oid == oid:
                self._session[idx] = model
                return model
        raise BookNotFoundException(oid)

    @override
    def delete(self, oid: str) -> None:
        for idx, book in enumerate(self._session):
            if book.oid == oid:
                del self._session[idx]
                return
        raise BookNotFoundException(oid)

    @override
    def list(self) -> List[Book]:
        return self._session
