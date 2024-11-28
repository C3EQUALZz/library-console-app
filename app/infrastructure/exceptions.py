from abc import ABC
from dataclasses import dataclass
from typing import Any

from app.exceptions import ApplicationException


@dataclass(eq=False)
class InfrastructureException(ApplicationException, ABC):
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
    value: Any

    @property
    def message(self) -> str:
        return f"Book {self.value} not found"


@dataclass(eq=False)
class InstanceException(InfrastructureException):
    value: Any

    @property
    def message(self) -> str:
        return f"{self.value}"
