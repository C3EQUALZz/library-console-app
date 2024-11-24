from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "An application error has occurred"

    def __str__(self) -> str:
        return self.message
