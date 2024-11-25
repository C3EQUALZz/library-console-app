from typing import List, Optional

from app.domain.entities.books import Book
from app.infrastructure.services.books import BooksService
from app.logic.commands.books import (CreateBookCommand, DeleteBookCommand,
                                      GetAllBooksCommand, GetBookByIdCommand,
                                      GetBookByTitleAndAuthorCommand,
                                      GetBookByTitleCommand, UpdateBookCommand)
from app.logic.exceptions import (BookAlreadyExistsException,
                                  BookNotExistsException)
from app.logic.handlers.books.base import BooksCommandHandler


class CreateBookCommandHandler(BooksCommandHandler):
    """
    Handler for creating a book which must be linked with CreateBookCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: CreateBookCommand) -> Book:
        """
        Create a new book, if book with provided credentials doesn't exist, and creates event signaling that
        operation was successfully executed.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the created book
        """

        books_service: BooksService = BooksService(uow=self._uow)

        if books_service.check_existence(title=command.title):
            raise BookAlreadyExistsException(command.title)

        book: Book = Book(**command.to_dict())

        return books_service.add(book=book)


class UpdateBookCommandHandler(BooksCommandHandler):
    def __call__(self, command: UpdateBookCommand) -> Book:
        """
        Updates a book, if book with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(title=command.title):
            raise BookNotExistsException()

        book: Book = Book(**command.to_dict())

        return books_service.update(book=book)


class DeleteBookCommandHandler(BooksCommandHandler):
    def __call__(self, command: DeleteBookCommand) -> None:
        """
        Deletes a book, if book with provided credentials exist. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: nothing
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(title=command.title):
            raise BookNotExistsException()

        book = books_service.get_by_title_and_author(title=command.title, author=command.author)

        return books_service.delete(oid=book.oid)


class GetBookByIdCommandHandler(BooksCommandHandler):
    def __call__(self, command: GetBookByIdCommand) -> Optional[Book]:
        """

        :param command:
        :return:
        """
        books_service: BooksService = BooksService(uow=self._uow)
        book = books_service.get_by_id(command.book_id)
        if not book:
            raise BookNotExistsException()
        return book


class GetBookByTitleCommandHandler(BooksCommandHandler):
    def __call__(self, command: GetBookByTitleCommand) -> Optional[Book]:
        books_service: BooksService = BooksService(uow=self._uow)
        book = books_service.get_by_title(command.title)
        if not book:
            raise BookNotExistsException()
        return book


class GetBookByTitleAndAuthorCommandHandler(BooksCommandHandler):
    def __call__(self, command: GetBookByTitleAndAuthorCommand) -> Optional[Book]:
        books_service: BooksService = BooksService(uow=self._uow)
        book = books_service.get_by_title_and_author(title=command.title, author=command.author)
        if not book:
            raise BookNotExistsException()
        return book


class GetAllBooksCommandHandler(BooksCommandHandler):
    def __call__(self, command: GetAllBooksCommand) -> List[Book]:
        books_service: BooksService = BooksService(uow=self._uow)
        return books_service.get_all()
