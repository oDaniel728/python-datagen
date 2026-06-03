from abc import ABC, abstractmethod

from datagen.function.function import Function

class Command(ABC):

    def __init__(self):
        if Function.__current_function:
            Function.__current_function.add_command(self)

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
        return f"${command}" if not command.startswith("$") else command

    def auto_macro(self, command: str) -> str:
        return self.to_macro(command) if self.is_macro(command) else command