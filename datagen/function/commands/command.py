from abc import ABC, abstractmethod
from typing import Self


class Command(ABC):

    silent = False

    @staticmethod
    def toggle_silent(value: bool | None = None):
        if value == None:
            Command.silent = not Command.silent
        else:
            Command.silent = value

    def __init__(self):
        pass

    def __invert__(self):
        from datagen.function.function import Function
        current_function = getattr(Function, "_Function__current_function", None)
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
        # removes macro and comments
        return "".join(line for line in self.rem_macro().splitlines() if not line.strip().startswith("#"))