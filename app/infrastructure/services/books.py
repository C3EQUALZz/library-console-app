from typing import (
    List,
    Optional,
)

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
        """
        Service method which adds a book in our database
        :param book: new book (domain object)
        :return: domain object if it was successfully added
        """
        with self._uow as uow:
            new_book = uow.books.add(model=book)
            uow.commit()
            return new_book

    def check_existence(self, oid: Optional[str] = None, title: Optional[str] = None) -> bool:
        """
        Service method which checks if a book exists in our database
        :param oid: unique identifier for the book
        :param title: name of the book
        :return: True if the book exists, False otherwise
        """
        if not (oid or title):
            return False

        with self._uow as uow:
            if oid and uow.books.get(oid):
                return True

            if title and uow.books.get_by_title(title):
                return True

        return False

    def get_by_title(self, title: str) -> Book:
        """
        Service method which gets a book by its title
        :param title: name of the book
        :return: books if the book was found, otherwise raises BookNotFoundException
        """
        with self._uow as uow:
            existing_book = uow.books.get_by_title(title)

            if not existing_book:
                raise BookNotFoundException(title)

            return existing_book

    def get_by_title_and_author(self, title: str, author: str) -> Book:
        """
        Service method which gets a book by its title and author
        :param title: name of the book
        :param author: author of the book
        :return: books if the book was found, otherwise raises BookNotFoundException
        """
        with self._uow as uow:
            existing_book = uow.books.get_by_title_and_author(title, author)

            if not existing_book:
                raise BookNotFoundException(f"with title: {title}, author: {author}")

            return existing_book

    def get_by_id(self, oid: str) -> Book:
        with self._uow as uow:
            existing_book = uow.books.get(oid)

            if not existing_book:
                raise BookNotFoundException(oid)

            return existing_book

    def get_all(self) -> List[Book]:
        with self._uow as uow:
            return uow.books.list()

    def update(self, book: Book) -> Book:
        with self._uow as uow:
            existing_book = uow.books.get(oid=book.oid)

            if not existing_book:
                raise BookNotFoundException(book.oid)

            updated_book = uow.books.update(oid=existing_book.oid, model=book)
            uow.commit()
            return updated_book

    def delete(self, oid: str) -> None:
        with self._uow as uow:
            existing_book = uow.books.get(oid)
            if not existing_book:
                raise BookNotFoundException(oid)
            uow.books.delete(oid)
            uow.commit()
