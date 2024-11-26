from dataclasses import (
    asdict,
    dataclass,
)
from typing import (
    Any,
    Optional,
)


@dataclass(frozen=True)
class BaseScheme:
    def model_dump(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CreateBookScheme(BaseScheme):
    title: str
    author: str
    year: int


@dataclass(frozen=True)
class UpdateBookScheme(BaseScheme):
    oid: str
    title: str
    author: str
    year: int
    status: str


@dataclass(frozen=True)
class ReadBookScheme(BaseScheme):
    oid: str


@dataclass(frozen=True)
class DeleteBookScheme(BaseScheme):
    oid: str


@dataclass(frozen=True)
class ReadAllBookScheme(BaseScheme):
    ...
