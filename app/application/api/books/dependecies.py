import logging
from typing import List

from app.application.api.books.schemas import (
    CreateBookScheme,
    DeleteBookScheme,
    ReadAllBookScheme,
    ReadBookScheme,
    UpdateBookScheme,
)
from app.domain.entities.books import Book
from app.exceptions import ApplicationException
from app.infrastructure.bootstrap import Bootstrap
from app.infrastructure.message_bus import MessageBus
from app.infrastructure.uow.books.jsonr import JsonBooksUnitOfWork
from app.logic.commands.books import (
    CreateBookCommand,
    DeleteBookCommand,
    GetAllBooksCommand,
    GetBookByIdCommand,
    UpdateBookCommand,
)
from app.logic.handlers import (
    COMMANDS_HANDLERS_FOR_INJECTION,
    EVENTS_HANDLERS_FOR_INJECTION,
)


logger = logging.getLogger(__name__)


def create(book_data: CreateBookScheme) -> Book:
    """
    Function which creates a book, it must be called using dependency injection.
    For example: it can be called using Depends from FastAPI.
    """
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(CreateBookCommand(**book_data.model_dump()))

        logger.info("Successfully created book [ %s ]", messagebus.command_result)

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        # This is done so that the console application does not go down.
        # If it were possible to use FastAPI, then HTTP Exception would be thrown here
        return  # type: ignore


def read(book_data: ReadBookScheme) -> Book:
    """
    Function which finds book, it must be called using dependency injection.
    For example: it can be called using Depends from FastAPI.
    """
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(GetBookByIdCommand(**book_data.model_dump()))

        logger.info("Successfully find book [ %s ]", messagebus.command_result)

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        # This is done so that the console application does not go down.
        # If it were possible to use FastAPI, then HTTP Exception would be thrown here
        return  # type: ignore


def read_all(_: ReadAllBookScheme) -> List[Book]:
    """
    Function which return all books in library, it must be called using dependency injection.
    For example: it can be called using Depends from FastAPI.
    """
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(GetAllBooksCommand())

        logger.info("Successfully read all books [ %s ]", messagebus.command_result)

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        # This is done so that the console application does not go down.
        # If it were possible to use FastAPI, then HTTP Exception would be thrown here
        return  # type: ignore


def update(book_data: UpdateBookScheme) -> Book:
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(UpdateBookCommand(**book_data.model_dump()))

        logger.info("Successfully updated book [ %s ]", messagebus.command_result)

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        # This is done so that the console application does not go down.
        # If it were possible to use FastAPI, then HTTP Exception would be thrown here
        return  # type: ignore


def delete(book_data: DeleteBookScheme) -> None:
    """
    Function which deletes a book, it must be called using dependency injection.
    For example: it can be called using Depends from FastAPI.
    """
    try:
        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION,
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(DeleteBookCommand(**book_data.model_dump()))

        logger.info("Successfully deleted book")

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)
        # This is done so that the console application does not go down.
        # If it were possible to use FastAPI, then HTTP Exception would be thrown here
        return  # type: ignore
