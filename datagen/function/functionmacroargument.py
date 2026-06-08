from typing import Any, Protocol

class _TConvertibleToString(Protocol):
    def __str__(self) -> str: ...

class FunctionMacroArgument[T: _TConvertibleToString]():
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
    def __init__(self, name: str) -> None:
        self.name = name

    def __getattribute__(self, name: str) -> FunctionMacroArgument[T]:
        return FunctionMacroArgument(f"{self.name}.{name}")

    def __str__(self) -> str:
        return f"$({self.name})"