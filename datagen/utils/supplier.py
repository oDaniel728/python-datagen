from typing import Callable


class Supplier[T]():
    def __init__(self, func: Callable[[], T]):
        self.func = func

    def get(self) -> T:
        return self.func()