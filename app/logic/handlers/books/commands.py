from typing import (
    List
)

from app.domain.entities.books import Book
from app.infrastructure.services.books import BooksService
from app.logic.commands.books import (
    CreateBookCommand,
    DeleteBookCommand,
    GetAllBooksCommand,
    GetBookByIdCommand,
    GetBookByTitleAndAuthorCommand,
    GetBookByTitleCommand,
    UpdateBookCommand,
)
from app.logic.exceptions import (
    BookAlreadyExistsException,
    BookNotExistsException, EmptyLibraryException,
)
from app.logic.handlers.books.base import BooksCommandHandler


class CreateBookCommandHandler(BooksCommandHandler[CreateBookCommand]):
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


class UpdateBookCommandHandler(BooksCommandHandler[UpdateBookCommand]):
    def __call__(self, command: UpdateBookCommand) -> Book:
        """
        Updates a book, if book with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(oid=command.oid):
            raise BookNotExistsException()

        book: Book = Book(**command.to_dict())

        return books_service.update(book=book)


class DeleteBookCommandHandler(BooksCommandHandler[DeleteBookCommand]):
    """
    Handler for deleting a book which must be linked with DeleteBookCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: DeleteBookCommand) -> None:
        """
        Deletes a book, if book with provided credentials exist. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: nothing
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(oid=command.oid):
            raise BookNotExistsException()

        return books_service.delete(oid=command.oid)


class GetBookByIdCommandHandler(BooksCommandHandler[GetBookByIdCommand]):
    """
    Handler for finding book using ID, this handler must be linked with GetBookByIdCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: GetBookByIdCommand) -> Book:
        """
        Gets book by ID, if book with provided credentials exist. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the book
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(oid=command.oid):
            raise BookNotExistsException()

        return books_service.get_by_id(oid=command.oid)


class GetBookByTitleCommandHandler(BooksCommandHandler[GetBookByTitleCommand]):
    """
    Handler for finding book using Title, this handler must be linked with GetBookByTitleCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: GetBookByTitleCommand) -> Book:
        """
        Gets book by title, if book with provided credentials exist. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the book
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(title=command.title):
            raise BookNotExistsException()

        return books_service.get_by_title(command.title)


class GetBookByTitleAndAuthorCommandHandler(BooksCommandHandler[GetBookByTitleAndAuthorCommand]):
    """
    Handler for finding book using title and author,
    this handler must be linked with GetBookByTitleAndAuthorCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: GetBookByTitleAndAuthorCommand) -> Book:
        """
        Gets book by title and author, if book with provided credentials exist. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the book
        """
        books_service: BooksService = BooksService(uow=self._uow)

        if not books_service.check_existence(title=command.title):
            raise BookNotExistsException()

        return books_service.get_by_title_and_author(title=command.title, author=command.author)


class GetAllBooksCommandHandler(BooksCommandHandler[GetAllBooksCommand]):
    """
    Handler for finding all books, this handler must be linked with GetAllBooksCommand in app/logic/handlers/__init__
    """

    def __call__(self, command: GetAllBooksCommand) -> List[Book]:
        """
        Get the list of all books in library. If there are no books, raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: list of domain entities of the books
        """
        books_service: BooksService = BooksService(uow=self._uow)

        library: List[Book] = books_service.get_all()

        if not library:
            raise EmptyLibraryException()

        return library
