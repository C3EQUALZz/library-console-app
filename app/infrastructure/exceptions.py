from app.exceptions import ApplicationException
from dataclasses import dataclass


@dataclass(eq=False)
class InfrastructureException(ApplicationException):
    @property
    def message(self) -> str:
        return "An infrastructure error has occurred"


@dataclass(eq=False)
class MessageBusMessageException(InfrastructureException):
    @property
    def message(self) -> str:
        return "Message bus message should be eiter of Event type, or Command type"


@dataclass(eq=False)
class BookNotFoundException(InfrastructureException):
    @property
    def message(self) -> str:
        return "Book not found"
