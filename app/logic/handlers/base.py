from abc import ABC, abstractmethod
from typing import Any

from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent


class AbstractHandler(ABC):

    @abstractmethod
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        raise NotImplementedError


class AbstractEventHandler(AbstractHandler, ABC):
    """
    Abstract event handler class, from which every event handler should be inherited from.
    """

    @abstractmethod
    def __call__(self, event: AbstractEvent) -> None:
        raise NotImplementedError


class AbstractCommandHandler(AbstractHandler, ABC):
    """
    Abstract command handler class, from which every command handler should be inherited from.
    """

    @abstractmethod
    def __call__(self, command: AbstractCommand) -> Any:
        raise NotImplementedError
