from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.books import Title, Author, Year, Status


@dataclass(eq=False)
class Book(BaseEntity):
    title: Title
    author: Author
    year: Year
    status: Status = "in-stock"

    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__
