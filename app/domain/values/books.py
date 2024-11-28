import re
from dataclasses import dataclass
from datetime import datetime
from typing import (
    Final,
    override,
)

from app.domain.exceptions import (
    BadNameFormatException,
    EmptyTextException,
    FakeYearException,
    InvalidBookStatus,
    ObsceneTextException,
    ValueTooLongException,
)
from app.domain.utils.enums import BookStatusEnum
from app.domain.values.base import BaseValueObject


RUSSIAN_SWEAR_WORDS_PATTERN: Final[str] = (
    r"(?iu)(?<![а-яё])(?:(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|"
    r"(?:\S(?=[а-яё]))+?[оаеи-])-?)?(?:[её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|и[пб][ае][тцд][ьъ]).*?|(?:(?"
    r":н[иеа]|(?:ра|и)[зс]|[зд]?[ао](?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч|в[ъы]?|пр[еи])-?)?ху(?:[яйиеёю]|л+и(?!ган))"
    r".*?|бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|\S*?(?:п(?:[иеё]зд|ид[аое]?р|ед(?:р(?!о)|[аое]р|ик)|охую)|бля(?:[дбц]|тс)|"
    r"[ое]ху[яйиеё]|хуйн).*?|(?:о[тб]?|про|на|вы)?м(?:анд(?:[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|"
    r"[ауи])?|е[нт]ь|ища)|уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|[ао]л[ао]ф[ьъ](?:[яиюе]|[еёо]й))|елд[ауые].*?|ля[тд]ь|"
    r"(?:[нз]а|по)х)(?![а-яё])"
)

AUTHOR_FULL_NAME_PATTERN: Final[str] = (
    r"^([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?\s+([А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)(\s+[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?)"
    r"?)|([A-Z][a-z]+(-[A-Z][a-z]+)?\s+([A-Z][a-z]+(-[A-Z][a-z]+)?)(\s+[A-Z][a-z]+(-[A-Z][a-z]+)?)?)$"
)


@dataclass(frozen=True)
class Title(BaseValueObject[str]):
    """
    Value object which associated with the book name
    """
    value: str

    @override
    def validate(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptyTextException()

        if len(self.value) > 100:
            raise ValueTooLongException(self.value)

        if re.match(RUSSIAN_SWEAR_WORDS_PATTERN, self.value):
            raise ObsceneTextException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Author(BaseValueObject[str]):
    """
    Value object which associated with the book author
    """
    value: str

    @override
    def validate(self) -> None:
        if not self.value or not self.value.strip():
            raise EmptyTextException()

        if len(self.value) > 100:
            raise ValueTooLongException(self.value)

        if not re.match(AUTHOR_FULL_NAME_PATTERN, self.value):
            raise BadNameFormatException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value


@dataclass(frozen=True)
class Year(BaseValueObject[int]):
    """
    Value object which associated with the year of writing the book
    """
    value: int

    @override
    def validate(self) -> None:
        if self.value < 1000 or self.value > datetime.today().year:
            raise FakeYearException(self.value)

    @override
    def as_generic_type(self) -> int:
        return self.value


@dataclass(frozen=True)
class Status(BaseValueObject[str]):
    """
    Value object which associated with the book status
    """
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
