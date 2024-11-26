from dataclasses import dataclass
from uuid import UUID

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class CreateBookCommand(AbstractCommand):
    title: str
    author: str
    year: int
    status: str = "in stock"


@dataclass(frozen=True)
class UpdateBookCommand(AbstractCommand):
    oid: str
    title: str
    author: str
    year: int
    status: str


@dataclass(frozen=True)
class DeleteBookCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class GetBookByIdCommand(AbstractCommand):
    oid: str


@dataclass(frozen=True)
class GetBookByTitleCommand(AbstractCommand):
    title: str


@dataclass(frozen=True)
class GetBookByTitleAndAuthorCommand(AbstractCommand):
    title: str
    author: str


@dataclass(frozen=True)
class GetAllBooksCommand(AbstractCommand):
    pass
