from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID
from app.domain.entities.base import BaseEntity


@dataclass
class AbstractRepository(ABC):
    """
    Interface for any repository, which would be used for work with domain model, according DDD.

    Main purpose is to encapsulate internal logic that is associated with the use of one or another data
    storage scheme, for example, ORM.
    """

    @abstractmethod
    def add(self, model: BaseEntity) -> BaseEntity:
        raise NotImplementedError

    @abstractmethod
    def get(self, oid: UUID) -> Optional[BaseEntity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, oid: UUID, model: BaseEntity) -> BaseEntity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, oid: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[BaseEntity]:
        raise NotImplementedError
