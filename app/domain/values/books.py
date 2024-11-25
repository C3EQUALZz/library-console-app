import re
from dataclasses import dataclass
from datetime import datetime
from typing import (
    NoReturn,
    override,
)

from app.domain.exceptions import (
    BadNameFormatException,
    EmptyTextException,
    FakeYearException,
    InvalidBookStatus,
    ValueTooLongException,
)
from app.domain.utils.enums import BookStatusEnum
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Title(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 100:
            raise ValueTooLongException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Author(BaseValueObject):
    value: str

    pattern = (
        r"^([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?\s+([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)(\s+[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)"
        r"?)|([A-Z][a-z]+(-[A-Z][a-z]+)?\s+([A-Z][a-z]+(-[A-Z][a-z]+)?)(\s+[A-Z][a-z]+(-[A-Z][a-z]+)?)?)$"
    )

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 100:
            raise ValueTooLongException(self.value)

        if not re.match(self.pattern, self.value) is not None:
            raise BadNameFormatException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Year(BaseValueObject):
    value: int

    @override
    def validate(self) -> None:
        if self.value < 1000 or self.value > datetime.today().year:
            raise FakeYearException(self.value)

    @override
    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class Status(BaseValueObject):
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if not self.value in set(BookStatusEnum.__members__.values()):
            raise InvalidBookStatus(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value
