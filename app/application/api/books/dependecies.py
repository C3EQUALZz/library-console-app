import logging

from app.application.api.books.schemas import CreateBookScheme, UpdateBookScheme, DeleteBookScheme
from app.domain.entities.books import Book
from app.exceptions import ApplicationException
from app.infrastructure.bootstrap import Bootstrap
from app.infrastructure.message_bus import MessageBus
from app.infrastructure.uow.books.jsonr import JsonBooksUnitOfWork
from app.logic.commands.books import CreateBookCommand, UpdateBookCommand, DeleteBookCommand
from app.logic.handlers import EVENTS_HANDLERS_FOR_INJECTION, COMMANDS_HANDLERS_FOR_INJECTION

logger = logging.getLogger(__name__)


def create(book_data: CreateBookScheme) -> Book:
    try:

        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(
            CreateBookCommand(
                **book_data.model_dump()
            )
        )

        return messagebus.command_result

    except ApplicationException as e:
        logger.error(e.message)


def update(book_data: UpdateBookScheme) -> Book:
    try:

        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(
            UpdateBookCommand(
                **book_data.model_dump()
            )
        )

        return messagebus.command_result

    except ApplicationException as e:
        logging.exception(e.message)


def delete(book_data: DeleteBookScheme) -> None:
    try:

        bootstrap: Bootstrap = Bootstrap(
            uow=JsonBooksUnitOfWork(),
            events_handlers_for_injection=EVENTS_HANDLERS_FOR_INJECTION,
            commands_handlers_for_injection=COMMANDS_HANDLERS_FOR_INJECTION
        )

        messagebus: MessageBus = bootstrap.get_messagebus()

        messagebus.handle(
            DeleteBookCommand(
                **book_data.model_dump()
            )
        )

        return messagebus.command_result

    except ApplicationException as e:
        logging.exception(e.message)


if __name__ == '__main__':
    print(
        delete(
            DeleteBookScheme(
                title="Василий Теркин",
                author="Александр Твардовский",
                year=2011
            )
        )
    )
