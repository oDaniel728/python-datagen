from abc import ABC, abstractmethod
import re
from typing import TYPE_CHECKING, Final

from datagen.types.util.counter import Counter

if TYPE_CHECKING:
    from datagen.function.commands._data.datastorage import DataStorageValue
    from datagen.utils.scoreboard.player import ScoreboardPlayer

_C = Counter()

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

    _LMACRO_EXPR: Final[str] = r"\$\(\w+\)"
    _LMACRO_START: Final[str] = r"\$"
    def is_macro(self, *args: str):
        for arg in args:
            if re.search(self._LMACRO_EXPR, arg):
                return True
        return False
    
    def __str__(self) -> str:
        return self.auto_macro(self.to_string())

    def to_macro(self, command: str) -> str:
        lines = command.splitlines(keepends=True)
        for i, line in enumerate(lines):
            if self.is_macro(line) and not line.lstrip().startswith("$"):
                lines[i] = re.sub(r"(\s*)([\w][^#])(.*)", r"\1$\2\3", line)
        return "".join(lines)

    def auto_macro(self, command: str) -> str:
        if self.is_macro(command):
            return self.to_macro(command)
        return command
    
    def rem_macro(self) -> str:
        return self.to_string().strip().replace("$", "", 1)
    
    def rem_comments(self) -> str:
        return "\n".join(line for line in self.to_string().splitlines() if not line.strip().startswith("#"))
    
    def raw(self) -> str:
        """Returns the raw string representation of the command, without any macro processing or comments. This can be useful for debugging or for cases where the original command string is needed without any modifications."""
        # removes macro and comments
        return "".join(line for line in self.rem_macro().splitlines() if not line.strip().startswith("#"))

    def encapsulate(self, name: str | None = None):
        """Encapsulates the command in a function, which allows for the command to be executed as a single unit. This is useful for commands that need to be executed together or for commands that need to be stored and reused later. The encapsulated function is given a unique name based on a counter to avoid naming conflicts."""
        from datagen.function.function import Function
        from datagen.datapack.namespace import Namespace
        f = Function(Namespace.temp() / (name or f"__encaps{_C}")).add_command(self)
        return f
    
    def into(self, holder: "DataStorageValue | ScoreboardPlayer") -> "Command":
        """Returns a command that stores the result of this command into the given holder, which can be a DataStorageValue or a ScoreboardPlayer. This allows for the result of the command to be used later in the function or in other commands."""
        from datagen.function.commands._data.datastorage import DataStorageValue
        from datagen.utils.scoreboard.player import ScoreboardPlayer
        if isinstance(holder, DataStorageValue):
            return holder.set(self)
        elif isinstance(holder, ScoreboardPlayer):
            return holder.set(self)
        else:
            raise TypeError(f"Cannot return into {type(holder)}")
