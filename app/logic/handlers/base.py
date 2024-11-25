from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent


class AbstractHandler(ABC):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError


ET = TypeVar("ET", bound=AbstractEvent)


class AbstractEventHandler(AbstractHandler, ABC, Generic[ET]):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __call__(self, event: ET) -> None:
        raise NotImplementedError


CT = TypeVar("CT", bound=AbstractCommand)


class AbstractCommandHandler(AbstractHandler, ABC, Generic[CT]):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    def __call__(self, command: CT) -> Any:
        raise NotImplementedError
