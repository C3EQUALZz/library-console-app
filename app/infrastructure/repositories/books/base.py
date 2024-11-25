from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    List,
    Optional,
)

from app.domain.entities.base import BaseEntity
from app.domain.entities.books import Book
from app.infrastructure.repositories.base import AbstractRepository


class BooksRepository(AbstractRepository[Book], ABC):
    """
    An interface for work with books, that is used by books unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    def get_by_title(self, title: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def get_by_title_and_author(self, title: str, author: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: BaseEntity) -> Book:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: str, model: BaseEntity) -> Book:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Book]:
        raise NotImplementedError
