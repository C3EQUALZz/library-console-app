from abc import ABC
from typing import List, Optional, override

from app.domain.entities.base import BaseEntity
from app.domain.entities.books import Book
from app.infrastructure.exceptions import (BookNotFoundException,
                                           InstanceException)
from app.infrastructure.repositories.base import AbstractRepository
from app.infrastructure.repositories.books.base import BooksRepository


class JsonAbstractRepository(AbstractRepository, ABC):
    """
    Repository interface for json, from which should be inherited all other repositories.
    """

    def __init__(self, session: List) -> None:
        self._session = session


class JsonBooksRepository(JsonAbstractRepository, BooksRepository):
    @override
    def __init__(self, session: List) -> None:
        super().__init__(session)

    @override
    def get_by_title(self, title: str) -> Optional[Book]:
        for item in self._session:
            if item["title"] == title:
                return Book(**item)
        return None

    @override
    def get_by_title_and_author(self, title: str, author: str) -> Optional[Book]:
        for item in self._session:
            if item["title"] == title and item["author"] == author:
                return Book(**item)
        return None

    @override
    def add(self, model: BaseEntity) -> Book:
        if not isinstance(model, Book):
            raise InstanceException("Only Book instances can be added to the repository.")
        book_data = model.__dict__
        self._session.append(book_data)
        return model

    @override
    def get(self, oid: str) -> Optional[Book]:
        for item in self._session:
            if item["oid"] == oid:
                return Book(**item)
        return None

    @override
    def update(self, oid: str, model: BaseEntity) -> Book:
        if not isinstance(model, Book):
            raise InstanceException("Only Book instances can be updated in the repository.")
        for idx, item in enumerate(self._session):
            if item["oid"] == str(oid):
                self._session[idx] = model.__dict__
                return model
        raise BookNotFoundException(oid)

    @override
    def delete(self, oid: str) -> None:
        for idx, item in enumerate(self._session):
            if item["oid"] == str(oid):
                del self._session[idx]
                return
        raise BookNotFoundException(oid)

    @override
    def list(self) -> List[Book]:
        return [Book(**item) for item in self._session]
