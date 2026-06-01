from typing import Protocol


class ToString(Protocol):
    def to_string(self) -> str: ...