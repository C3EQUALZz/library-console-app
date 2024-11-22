from dataclasses import dataclass

from app.domain.values.books import Title, Author, Year, Status


@dataclass(eq=False)
class Book:
    title: Title
    author: Author
    year: Year
    status: Status

