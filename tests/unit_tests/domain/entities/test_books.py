import pytest

from app.domain.entities.books import Book
from app.domain.values.books import Title, Author, Year, Status


@pytest.mark.parametrize("title, author, year, status", [
    (Title("1984"), Author("George Orwell"), Year(1949), Status("in stock")),
    (Title("Brave New World"), Author("Aldous Huxley"), Year(1932), Status("in stock")),
    (Title("Fahrenheit 451"), Author("Ray Bradbury"), Year(1953), Status("in stock")),
])
def test_books_creating_and_the_instance_was_created_correctly_if_the_arguments_are_passed_by_name(
        title,
        author,
        year,
        status
) -> None:
    book = Book(title=title, author=author, year=year, status=status)

    assert book.title == title
    assert book.author == author
    assert book.year == year
    assert book.status == status


@pytest.mark.parametrize("book_mapping", [
    ({"title": "1984", "author": "George Orwell", "year": 1949, "status": "in stock"}),
    ({"title": "Brave New World", "author": "Aldous Huxley", "year": 1932, "status": "in stock"}),
    ({"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953, "status": "in stock"}),
])
def test_books_creating_and_the_instance_was_created_correctly_if_the_arguments_are_passed_by_unpacking_the_dictionary(
        book_mapping
) -> None:
    book = Book(**book_mapping)

    assert book.title.as_generic_type() == book_mapping["title"]
    assert book.author.as_generic_type() == book_mapping["author"]
    assert book.year.as_generic_type() == book_mapping["year"]
    assert book.status.as_generic_type() == book_mapping["status"]


@pytest.mark.parametrize("book_mapping", [
    ({"title": "1984", "author": "George Orwell", "year": 1949}),
    ({"title": "Brave New World", "author": "Aldous Huxley", "year": 1932}),
    ({"title": "Fahrenheit 451", "author": "Ray Bradbury", "year": 1953}),
])
def test_books_creating_and_checking_default_status(book_mapping) -> None:
    book = Book(**book_mapping)

    assert book.status.value == "in stock"
