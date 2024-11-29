from datetime import datetime
from typing import Optional

import pytest
from app.domain.exceptions import (
    BadNameFormatException,
    EmptyTextException,
    FakeYearException,
    InvalidBookStatus,
    ObsceneTextException,
    ValueTooLongException,
)
from app.domain.values.books import (
    Author,
    Status,
    Title,
    Year,
)
from faker import Faker


@pytest.mark.parametrize("long_title", [
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=256) for _ in range(10))),
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=300) for _ in range(10))),
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=500) for _ in range(10))),
])
def test_title_long_name_raises_exception(long_title: str) -> None:
    with pytest.raises(ValueTooLongException):
        Title(long_title)


@pytest.mark.parametrize("title", [
    None,
    *[" " * i for i in range(10)]
])
def test_title_empty_raises_exception(title: Optional[str]) -> None:
    with pytest.raises(EmptyTextException):
        Title(title)


@pytest.mark.parametrize("title", [
    "хуй",
    "блять",
    "пизда",
    "пиздец",
    "хуйня",
    "хупизда",
    "пиздюлина"
])
def test_title_with_obscene_raises_exception(title: str) -> None:
    with pytest.raises(ObsceneTextException):
        Title(title)


@pytest.mark.parametrize("long_name", [
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=256) for _ in range(10))),
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=300) for _ in range(10))),
    *filter(lambda text: len(text) > 100, (Faker().text(max_nb_chars=500) for _ in range(10))),
])
def test_author_full_name_raises_exception(long_name: str) -> None:
    with pytest.raises(ValueTooLongException):
        Author(long_name)


@pytest.mark.parametrize("name", [
    None,
    "",
    *(" " * i for i in range(10))
])
def test_author_empty_raises_exception(name: Optional[str]) -> None:
    with pytest.raises(EmptyTextException):
        Author(name)


@pytest.mark.parametrize("name", [
    *(Faker().first_name_male() for _ in range(10)),
    *(Faker().last_name_male() for _ in range(10)),
    *(Faker().file_path() for _ in range(10)),
    *(Faker().phone_number() for _ in range(10)),
    *(Faker().email() for _ in range(10)),
])
def test_author_bad_name_raises_exception(name: str) -> None:
    with pytest.raises(BadNameFormatException):
        Author(name)


@pytest.mark.parametrize("year", [
    *filter(lambda y: y < 1000 or y > datetime.today().year, (int(Faker().year()) for _ in range(50))),
])
def test_fake_year_raises_exception(year: int) -> None:
    with pytest.raises(FakeYearException):
        Year(year)


@pytest.mark.parametrize("status", [
    *(Faker().text() for _ in range(10)),
])
def test_fake_status_raises_exception(status: str) -> None:
    with pytest.raises(InvalidBookStatus):
        Status(status)
