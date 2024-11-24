from dataclasses import dataclass

from app.exceptions import ApplicationException


@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def message(self) -> str:
        return "An logic error has occurred"


@dataclass(eq=False)
class BookNotExistsException(LogicException):
    @property
    def message(self) -> str:
        return "Book does not exists"


@dataclass(eq=False)
class BookAlreadyExistsException(LogicException):
    value: str = ""

    @property
    def message(self) -> str:
        return f"Book {self.value} already exists"
