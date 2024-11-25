from dataclasses import dataclass, field
from typing import List, Optional, override
from uuid import UUID

from app.domain.entities.books import Book
from app.infrastructure.repositories.books.base import BooksRepository


@dataclass
class MemoryBookRepository(BooksRepository):
    _saved_books: list[Book] = field(default_factory=list, kw_only=True)

    @override
    def get_by_title(self, title: str) -> Optional[Book]:
        try:
            return next(
                book for book in self._saved_books if book.title.as_generic_type() == title
            )
        except StopIteration:
            return None

    @override
    def add(self, book: Book) -> Book:
        self._saved_books.append(book)
        return book

    @override
    def get(self, oid: int) -> Optional[Book]:
        try:
            return next(
                book for book in self._saved_books if book.oid == oid
            )
        except StopIteration:
            return None

    @override
    def update(self, oid: UUID, model: Book) -> Book:
        for idx, book in enumerate(self._saved_books):
            if book.oid == oid:
                self._saved_books[idx] = model
                return model

    @override
    def delete(self, oid: UUID) -> None:
        for idx, book in enumerate(self._saved_books):
            if book.oid == oid:
                self._saved_books.pop(idx)

    @override
    def list(self) -> List[Book]:
        return self._saved_books.copy()
