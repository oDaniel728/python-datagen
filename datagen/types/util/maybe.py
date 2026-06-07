class Maybe[T]():
    def __init__(self, value: T | None = None) -> None:
        self.value = value

    def exists(self) -> bool:
        return self.value is not None
    
    def get(self) -> T:
        return self.value # type: ignore
    
    def __neg__(self) -> T:
        return self.get()
    
    def __invert__(self) -> T | None:
        return self.value

    def __or__[U](self, other: U) -> T | U:
        return self.get() if self.exists() else other