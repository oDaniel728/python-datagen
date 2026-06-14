from abc import ABC, abstractmethod
from typing import Self

from datagen.globals import DatagenConfig


class Command(ABC):
    """
    # Command
    - See https://minecraft.wiki/w/Commands
    ## Summary
    Represents a Minecraft command, which is a single instruction that can be executed in the game.
    ## Examples
    - Creating a command
    ```python
    with Function(Identifier.of("pack:example")) as f:
        ~ Say("This is a command!") # Say inherits from Command, 
        # so it can be added to a function using the ~ operator
    ```
    """

    silent = False

    @staticmethod
    def toggle_silent(value: bool | None = None):
        if value == None:
            Command.silent = not Command.silent
        else:
            Command.silent = value

    def __init__(self) -> None:
        pass

    def __invert__(self):
        """Adds the command to the currently active function being built, if there is one and if the command is not set to silent. This allows for a convenient syntax for adding commands to functions using the `~` operator, while also providing the option to create commands that do not automatically add themselves to the current function if desired."""
        from datagen.function.function import Function
        current_function: "Function" = getattr(Function, "current_function", None) # type: ignore
        if current_function and not self.silent:
            current_function.add_command(self)

    @abstractmethod
    def to_string(self) -> str: ...

    def is_macro(self, *args: str):
        for arg in args:
            if '$' in arg:
                return True
        return False
    
    def __str__(self) -> str:
        if not DatagenConfig.config["builderSettings"]["comment"]:
            return self.auto_macro(self.rem_comments())
        return self.auto_macro(self.to_string())

    def to_macro(self, command: str) -> str:
        if (self.is_macro(command)):
            return ("\n"+command).replace("\n", "\n$").replace("$#", "#")
        return command

    def auto_macro(self, command: str) -> str:
        return self.to_macro(command) if self.is_macro(command) else command
    
    def rem_macro(self) -> str:
        return self.to_string().replace("$", "", 1) if not self.is_macro(self.to_string()) else self.to_string()
    
    def rem_comments(self) -> str:
        return "\n".join(line for line in self.to_string().splitlines() if not line.strip().startswith("#"))
    
    def raw(self) -> str:
        """Returns the raw string representation of the command, without any macro processing or comments. This can be useful for debugging or for cases where the original command string is needed without any modifications."""
        # removes macro and comments
        return "".join(line for line in self.rem_macro().splitlines() if not line.strip().startswith("#"))