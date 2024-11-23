from abc import ABC, abstractmethod
from typing import Self, List, Generator
from app.logic.events.base import AbstractEvent
from dataclasses import dataclass, field


@dataclass
class AbstractUnitOfWork(ABC):
    """
    Interface for any units of work, which would be used for transaction atomicity, according DDD.
    """
    _events: List[AbstractEvent] = field(default_factory=list)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.rollback()

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError

    def add_event(self, event: AbstractEvent) -> None:
        self._events.append(event)

    def get_events(self) -> Generator[AbstractEvent, None, None]:
        """
        Using generator to get elements only when they needed.
        Also can not use self._events directly, not to run events endlessly.
        """

        while self._events:
            yield self._events.pop(0)

