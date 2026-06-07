from typing import Protocol

class _TConvertibleToString(Protocol):
    def __str__(self) -> str: ...

class FunctionMacroArgument[T: _TConvertibleToString]():
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"$({self.name})"