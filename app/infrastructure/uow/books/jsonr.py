import json
import os
from pathlib import Path
from typing import (
    Any,
    List,
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
    Unit of work interface for Json, from which should be inherited all other units of work.
    """

    @override
    def __init__(self, file_path: os.PathLike[str] | str = settings.path_to_database_json_file) -> None:
        super().__init__()

        self._data: List[Book] = []  # Хранилище объектов
        self._file_path = Path(file_path)
        self._backup: List[Book] = []

    @override
    def __enter__(self) -> Self:
        self._data = self.__load()
        self._backup = self._data.copy()

        return super().__enter__()

    @override
    def __exit__(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        if self._data != self._backup:
            self.commit()
        super().__exit__(*args, **kwargs)

    @override
    def commit(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self._data], f, ensure_ascii=False, indent=4)

    @override
    def rollback(self) -> None:
        self._data = self._backup.copy()

    def __load(self) -> List[Book]:
        """
        Приватный метод для загрузки данных из файла и преобразования их в объекты Book.
        """
        if self._file_path.exists() and self._file_path.is_file():
            with open(self._file_path, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.load(f)
                    return [Book(**item) for item in raw_data]
                except json.JSONDecodeError:
                    return []


class JsonBooksUnitOfWork(JsonAbstractUnitOfWork, BooksUnitOfWork):
    """
    Implementation of json book uow.
    Here you must add only repositories for work
    """

    def __enter__(self) -> Self:
        uow = super().__enter__()
        self.books: BooksRepository = JsonBooksRepository(session=self._data)
        return uow
