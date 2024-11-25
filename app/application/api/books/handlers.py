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
    read_all
)

from app.application.api.books.schemas import (
    CreateBookScheme,
    DeleteBookScheme,
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
    author = input("Please write name of the author: ")
    title = input("Please write name of the book: ")
    year = int(input("Please write name of the year: "))

    delete(DeleteBookScheme(
        title=title,
        author=author,
        year=year
    ))


def read_book() -> None:
    print("Читаю книги")


def read_all_books() -> None:
    read_all(ReadAllBookScheme())
