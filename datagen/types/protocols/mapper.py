from typing import Callable, Protocol


class Mapper[I, O](Protocol):
    def map(self, value: I) -> O: ...