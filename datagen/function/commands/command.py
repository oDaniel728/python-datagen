from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def to_string(self) -> str: ...

    def is_macro(self, *args: str):
        for arg in args:
            if '$' in arg:
                return True
        return False
    
    def __str__(self) -> str:
        return self.to_string()

    def to_macro(self, command: str) -> str:
        return f"${command}" if not command.startswith("$") else command

    def auto_macro(self, command: str) -> str:
        return self.to_macro(command) if self.is_macro(command) else command