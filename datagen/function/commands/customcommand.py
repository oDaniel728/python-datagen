from datagen.function.commands.command import Command


class CustomCommand(Command):
    r"""
    # Custom Command \: Command
    ## Summary
    Represents a custom command that can be defined by the user. The command is defined by a string that can contain multiple lines, and can be added to a function using the `+=` operator or the `add_command` method. This class is useful for adding commands that do not have a specific class representation in the library, or for quickly adding raw command strings without needing to create a new command class.
    
    # Examples
    - Creating a custom command and adding it to a function
    ```python
    with Function(Identifier.of("pack:example")) as f:
        ~ CustomCommand("say Hello, world!")
    ```
    - Creating a custom command with multiple words
    ```python
    with Function(Identifier.of("pack:example")) as f:
        ~ CustomCommand("say", "Hello,", "world!")
    ```
    """
    def __init__(self, *command: str, prefix: str = "") -> None:
        super().__init__()
        self.command = (prefix + " ".join(command)).replace("\n ", "\n")
        self.prefix = prefix

    def to_string(self) -> str:
        return self.command
    
    def __add__(self, other: "Command | str") -> "CustomCommand":
        if isinstance(other, str):
            return CustomCommand(self.command + "\n" + other, prefix=self.prefix)
        else:
            return CustomCommand(self.command + "\n" + other.to_string(), prefix=self.prefix)
        
    def __iadd__(self, other: "Command | str") -> "CustomCommand":
        if isinstance(other, str):
            self.command += "\n" + other
        else:
            self.command += "\n" + other.to_string()
        return self