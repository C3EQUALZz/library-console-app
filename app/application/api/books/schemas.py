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
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    status: Optional[str] = None


@dataclass(frozen=True)
class ReadBookScheme(BaseScheme):
    title: str
    author: str


@dataclass(frozen=True)
class DeleteBookScheme(BaseScheme):
    title: str
    author: str
    year: int
