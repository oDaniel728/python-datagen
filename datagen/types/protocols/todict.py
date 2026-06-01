from typing import Protocol


class ToDict(Protocol):
    def to_dict(self) -> dict:
        ...