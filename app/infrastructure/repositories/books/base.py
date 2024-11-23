from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from app.domain.entities.base import BaseEntity
from app.infrastructure.repositories.base import AbstractRepository
from app.domain.entities.books import Book
from uuid import UUID


@dataclass
class BooksRepository(AbstractRepository, ABC):
    """
    An interface for work with books, that is used by books unit of work.
    The main goal is that implementations of this interface can be easily replaced in users unit of work
    using dependency injection without disrupting its functionality.
    """

    @abstractmethod
    def get_by_title(self, title: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def add(self, model: BaseEntity) -> Book:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: UUID) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: UUID, model: BaseEntity) -> Book:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Book]:
        raise NotImplementedError
