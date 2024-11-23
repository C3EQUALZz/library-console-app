from typing import Optional, List
from uuid import UUID
from app.domain.entities.books import Book
from app.infrastructure.exceptions import BookNotFoundException
from app.infrastructure.uow.books.base import BooksUnitOfWork


class BooksService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: BooksUnitOfWork) -> None:
        self._uow = uow

    def add(self, book: Book) -> Book:
        with self._uow as uow:
            new_book = uow.books.add(model=book)
            uow.commit()
            return new_book

    def check_existence(
            self,
            oid: Optional[UUID] = None,
            title: Optional[str] = None
    ) -> bool:
        if not (oid or title):
            return False

        with self._uow as uow:

            if oid and uow.books.get(oid):
                return True

            if title and uow.books.get_by_title(title):
                return True

        return False

    def get_by_title(self, title: str) -> Book:
        with self._uow as uow:
            return uow.books.get_by_title(title)

    def get_by_id(self, oid: UUID) -> Book:
        with self._uow as uow:
            return uow.books.get(oid)

    def get_all(self) -> List[Book]:
        with self._uow as uow:
            return uow.books.list()

    def update(self, book: Book) -> Book:
        with self._uow as uow:
            existing_book = uow.books.get(book.oid)
            if not existing_book:
                raise BookNotFoundException()
            updated_book = uow.books.update(oid=book.oid, model=book)
            uow.commit()
            return updated_book

    def delete(self, oid: UUID) -> None:
        with self._uow as uow:
            existing_book = uow.books.get(oid)
            if not existing_book:
                raise BookNotFoundException()
            uow.books.delete(oid)
            uow.commit()
