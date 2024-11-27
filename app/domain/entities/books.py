import logging

from dataclasses import dataclass, field

from app.domain.entities.base import BaseEntity
from app.domain.values.books import (
    Author,
    Status,
    Title,
    Year,
)


@dataclass(eq=False)
class Book(BaseEntity):
    """
    Domain object, which represents a book.
    It has several fields:

    - **title**: name of the book
    - **author**: author of the book
    - **year**: the year of writing the book
    - **status**: the status that indicates the presence or absence of the book
    """

    title: Title
    author: Author
    year: Year
    status: Status = field(default_factory=lambda: Status("in stock"))

    def __post_init__(self) -> None:
        super().__post_init__()
        logging.debug("Successfully initialized Book instance [%s]", self)

    __hash__ = BaseEntity.__hash__
    __eq__ = BaseEntity.__eq__
