"""
This is how the logic of the functions is written so that everything can be replaced here with handlers using FastAPI.
And I can call all functions using 'Depends' from FastAPI.

For example:

@app.post("/")
async def create_book(Depends(create)):
    ...

But the problem is that I wrote my code in sync mode, because application must be console....
"""

from app.application.api.books.dependecies import (
    create,
    delete,
    read,
    read_all
)

from app.application.api.books.schemas import (
    CreateBookScheme,
    DeleteBookScheme,
    ReadBookScheme,
    ReadAllBookScheme
)


def create_book() -> None:
    """
    Function that associated with handler create book
    """
    author = input("Please write name of the author: ")
    title = input("Please write name of the book: ")
    year = int(input("Please write name of the year: "))

    create(CreateBookScheme(
        author=author,
        title=title,
        year=year
    ))


def update_book() -> None:
    """
    Function that associated with handler update book
    """
    print("Обновляю книгу")


def delete_book() -> None:
    """
    Function that associated with handler delete book
    """
    oid = input("Please write id of the book: ")

    delete(DeleteBookScheme(
        oid=oid
    ))


def read_book() -> None:
    """
    Function that associated with handler read book (finds book by id)
    """
    oid = input("Please write id of the book: ")

    read(
        ReadBookScheme(
            oid=oid
        )
    )


def read_all_books() -> None:
    """
    Function that associated with handler read all books
    """
    read_all(ReadAllBookScheme())
