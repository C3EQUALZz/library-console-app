from queue import Queue
from typing import Any, Dict, List, Type, Union

from app.infrastructure.exceptions import MessageBusMessageException
from app.infrastructure.uow.base import AbstractUnitOfWork
from app.logic.commands.base import AbstractCommand
from app.logic.events.base import AbstractEvent
from app.logic.handlers.base import AbstractCommandHandler, AbstractEventHandler


class MessageBus:
    def __init__(
        self,
        uow: AbstractUnitOfWork,
        event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]],
        command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler],
    ) -> None:
        self._uow: AbstractUnitOfWork = uow
        self._event_handlers: Dict[Type[AbstractEvent], List[AbstractEventHandler]] = event_handlers
        self._command_handlers: Dict[Type[AbstractCommand], AbstractCommandHandler] = command_handlers
        self._queue: Queue = Queue()
        self._command_result: Any = None

    def handle(self, message: Union[AbstractEvent, AbstractCommand]) -> None:
        self._queue.put(message)
        while not self._queue.empty():
            message = self._queue.get()
            if isinstance(message, AbstractEvent):
                self._handle_event(event=message)
            elif isinstance(message, AbstractCommand):
                self._handle_command(command=message)
            else:
                raise MessageBusMessageException()

    def _handle_event(self, event: AbstractEvent) -> None:
        handler: AbstractEventHandler
        for handler in self._event_handlers[type(event)]:
            handler(event)
            for event in self._uow.get_events():
                self._queue.put_nowait(event)

    def _handle_command(self, command: AbstractCommand) -> None:
        handler: AbstractCommandHandler = self._command_handlers[type(command)]
        self._command_result = handler(command)
        for event in self._uow.get_events():
            self._queue.put_nowait(event)

    @property
    def command_result(self) -> Any:
        return self._command_result
