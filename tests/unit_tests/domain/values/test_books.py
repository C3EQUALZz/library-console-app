import pytest
from typing import Optional
from faker import Faker
from app.domain.exceptions import ValueTooLongException, EmptyTextException, ObsceneTextException
from app.domain.values.books import Title


@pytest.mark.parametrize("long_title", [
    Faker().text(max_nb_chars=256),
    Faker().text(max_nb_chars=300),
    Faker().text(max_nb_chars=500),
])
def test_title_long_name_raises_exception(long_title: str) -> None:
    with pytest.raises(ValueTooLongException):
        Title(long_title)


@pytest.mark.parametrize("title", [
    None,
    "",
    *[" " * i for i in range(0, 10)]
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
