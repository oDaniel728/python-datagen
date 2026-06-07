from typing import Protocol, runtime_checkable

@runtime_checkable
class ToDict(Protocol):
    def to_dict(self) -> dict:
        ...