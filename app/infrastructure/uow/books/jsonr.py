import json
import os
from pathlib import Path
from typing import (
    List,
    Optional,
    override,
    Self,
)

from app.domain.entities.books import Book
from app.infrastructure.repositories.books.base import BooksRepository
from app.infrastructure.repositories.books.jsonr import JsonBooksRepository
from app.infrastructure.uow.base import AbstractUnitOfWork
from app.infrastructure.uow.books.base import BooksUnitOfWork
from app.settings.config import settings


class JsonAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for SQLAlchemy, from which should be inherited all other units of work,
    which would be based on SQLAlchemy logics.
    """

    @override
    def __init__(self, file_path: os.PathLike[str] | str = settings.path_to_database_json_file) -> None:
        super().__init__()

        self._data: List[Book] = []
        self._file_path = Path(file_path)
        self._backup: str = ""

    @override
    def __enter__(self) -> Self:
        if self._file_path.exists() and self._file_path.is_file():
            with open(self._file_path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        else:
            self._data = []

        self._backup = json.dumps(self._data)

        return super().__enter__()

    @override
    def __exit__(self, *args, **kwargs) -> None:
        if self._data != json.loads(self._backup):
            self.commit()
        super().__exit__(*args, **kwargs)

    @override
    def commit(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=4)

    @override
    def rollback(self) -> None:
        self._data = json.loads(self._backup)


class JsonBooksUnitOfWork(JsonAbstractUnitOfWork, BooksUnitOfWork):
    def __enter__(self) -> Self:
        uow = super().__enter__()
        self.books: BooksRepository = JsonBooksRepository(session=self._data)
        return uow
