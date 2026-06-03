from datagen.function.commands.command import Command


class CustomCommand(Command):
    def __init__(self, *command: str) -> None:
        super().__init__()
        self.command = " ".join(command)

    def to_string(self) -> str:
        return self.command
    
    def __add__(self, other: "Command | str") -> "CustomCommand":
        if isinstance(other, str):
            return CustomCommand(self.command + "\n " + other)
        else:
            return CustomCommand(self.command + "\n " + other.to_string())
        
    def __iadd__(self, other: "Command | str") -> "CustomCommand":
        if isinstance(other, str):
            self.command += "\n " + other
        else:
            self.command += "\n " + other.to_string()
        return self