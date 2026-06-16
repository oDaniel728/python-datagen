from typing import Any, Protocol, Type, overload, runtime_checkable

@runtime_checkable
class _TConvertibleToString(Protocol):
    def __str__(self) -> str: ...

class FunctionMacroArgument[T: _TConvertibleToString = Any]():
    r"""
    # Function Macro Argument \<T\>
    \<T : __str__>
    ## Summary
    Represents an argument that can be passed to a function macro. The argument is defined by a

    ## Examples
    - Creating a function macro argument
    ```python
arg = FunctionMacroArgument("example")
print(arg)  # Output: $(example)
    ```
    - Using a function macro argument in a command
    ```python
    with Function(Identifier.of("pack:example")) as f:
        arg = FunctionMacroArgument("example")
        ~ Say(arg)
    ```

    """
    def __init__(self, path: str) -> None:
        self._path = path

    def __getattr__(self, name: str | int) -> FunctionMacroArgument[T]:
        if isinstance(name, int):
            return FunctionMacroArgument(f"{self._path}[{name}]")
        return FunctionMacroArgument(f"{self._path}.{name}")
    
    @overload
    def __getitem__[U](self, key: Type[U], /) -> FunctionMacroArgument[U]: ...
    @overload
    def __getitem__(self, key: int, /) -> FunctionMacroArgument[T]: ...
    @overload
    def __getitem__(self, key: _TConvertibleToString, /) -> FunctionMacroArgument[T]: ...

    def __getitem__(self, key: Any, /) -> Any:
        if isinstance(key, int):
            return FunctionMacroArgument(f"{self._path}[{key}]")
        elif isinstance(key, _TConvertibleToString):
            return FunctionMacroArgument(f"{self._path}.{str(key)}")
        else:
            return FunctionMacroArgument[key](f"{self._path}")

    def __str__(self) -> str:
        return f"$({self._path})"

    def to_score(self, set: bool = False):
        from datagen.utils.scoreboard.objective import ScoreboardObjective
        plr = (~ ScoreboardObjective.TEMP)["__" + self._path]
        if set:
            ~ plr.set(self)
        return plr