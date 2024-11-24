from abc import ABC
from dataclasses import dataclass, asdict, field
from typing import Optional, Any, Dict, Set
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):
    """
    Base model, from which any domain model should be inherited.
    """
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)

    async def to_dict(
            self,
            exclude: Optional[Set[str]] = None,
            include: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data

    def __eq__(self, other: "BaseEntity") -> bool:
        if not isinstance(other, BaseEntity):
            raise NotImplementedError
        return self.oid == other.oid

    def __hash__(self) -> int:
        return hash(self.oid)
