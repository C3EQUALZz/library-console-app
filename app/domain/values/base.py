from dataclasses import dataclass
from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Any, NoReturn

T = TypeVar("T", bound=Any)

@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[T]):
    value: T

    def __post_init__(self) -> NoReturn:
        self.validate()

    @abstractmethod
    def validate(self) -> NoReturn:
        ...

    @abstractmethod
    def as_generic_type(self) -> T:
        ...