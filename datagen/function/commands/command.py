from abc import ABC, abstractmethod


class Command(ABC):

    def __init__(self):
        from datagen.function.function import Function
        current_function = getattr(Function, "_Function__current_function", None)
        if current_function:
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
        return f"${command}" if not command.startswith("$") else command

    def auto_macro(self, command: str) -> str:
        return self.to_macro(command) if self.is_macro(command) else command