from typing import TYPE_CHECKING, Any, Self

from datagen.function.functionmacroargument import FunctionMacroArgument

if TYPE_CHECKING:
    from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.utils.minecraft.identifier import Identifier
from datagen.function.commands.command import Command
from datagen.globals import FUNCTIONS_PATH, DatagenConfig
from datagen.utils.simplefile import SimpleFile


class Function():
    """
    # Function
    - See https://minecraft.wiki/w/Function_(Java_Edition)

    ## Summary
    Represents a Minecraft function, which is a sequence of commands that can be executed together.

    ## Examples
    - Hello World Function
    ```python
# With with statements
with Function(Identifier.of("pack:hello")) as f:
    ~ Say("Hello, world!")
# Without with statements
f = Function(Identifier.of("pack:hello"))
f.add_command(Say("Hello, world!"))
    ```
    - Running a function
    ```
with Function(Identifier.of("pack:another")) as g:
    ~ f.run()
    # or
    ~ RunFunction(f)
    ```
    - Running a function with arguments
    ```
# With literal arguments
with Function(Identifier.of("pack:another")) as g:
    ~ f.run({"arg1": "value1", "arg2": 123})
    # or
    ~ RunFunction(f, {"arg1": "value1", "arg2": 123})

# With DataStorage arguments
with Function(Identifier.of("pack:another")) as g:
    args = DataStorage(Identifier.of("pack:__args"))
    ~ args.set_from_entity("self", TargetSelector.SELF)
    ~ f.run(args)
    # or
    ~ RunFunction(f, args)
    ```
    """
    current_function: Function | None = None
    functions = list["Function"]()

    @staticmethod
    def get_current_function() -> Function | None:
        """Returns the currently active function being built, or `None` if no function is currently active."""
        return Function.current_function
    
    @staticmethod
    def set_current_function(func: Function | None):
        """Sets the currently active function being built. This is used internally when entering and exiting a function context, and should not be called directly by users."""
        Function.current_function = func
        if func:
            Function.functions.append(func)

    @staticmethod
    def get_back_current_function() -> Function | None:
        """Reverts the currently active function to the previous one in the stack."""
        # undoes the current function
        # before: [A, B, C] with current C
        # after: [A, B] with current B
        if Function.current_function is not None:
            func = Function.current_function
            Function.current_function = None
            if func in Function.functions:
                Function.functions.remove(func)
            Function.current_function = Function.functions[-1] \
                if len(Function.functions) > 0 \
                else None
            return func
        else:
            return None

    fns = dict[Identifier, "Self"]()

    def __new__(cls, id: Identifier) -> Self:
        if id in cls.fns:
            return cls.fns[id]
        else:
            func = super(Function, cls).__new__(cls)
            cls.fns[id] = func
            return func

    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.get(id)

        self.commands = list[Command]()

    def __hash__(self) -> int:
        return hash(self.id)

    def add_command(self, command: Command) -> Self:
        """Adds a command to the function."""
        self.commands.append(command)
        return self
    
    def add_commands(self, *commands: Command) -> Self:
        """Adds multiple commands to the function."""
        for command in commands:
            self.add_command(command)
        return self

    def get_filepath(self):
        """Returns the file path where the function should be saved, based on its identifier and the configured functions path."""
        return FUNCTIONS_PATH + self.id._path.replace(".", "/").replace(" ", "_") + ".mcfunction"

    def to_string(self) -> str:
        """Converts the function to a string in the format of a Minecraft function file, with proper indentation and formatting."""
        lines: list[str] = []
        lines.append("# " + self.id._path)
        indent = " " * DatagenConfig.config["builderSettings"]["indent"]
        for command in self.commands:
            cmd_str = command.to_string()
            # remove only leading newlines to avoid accidental empty first line
            cmd_str = cmd_str.lstrip("\n")
            for line in cmd_str.splitlines():
                if line.strip() == "":
                    lines.append("")
                elif line.lstrip().startswith("#"):
                    # keep comment lines unindented
                    lines.append(line.lstrip())
                else:
                    # normalize existing leading whitespace and indent command lines
                    lines.append(indent + line.lstrip())
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.id.__str__()
    
    def to_file(self) -> SimpleFile:
        """Converts the function to a `SimpleFile` object, which can be used to write the function to disk. The file path is determined by the function's identifier and the configured functions path, and the content is generated by the `to_string` method."""
        return SimpleFile(self.get_filepath(), self.to_string())
    
    def __iadd__(self, command: Command) -> Self:
        """Adds a command to the function using the `+=` operator."""
        return self.add_command(command)
    
    def __enter__(self) -> "FunctionContext":
        """Enters the context of the function, setting it as the currently active function being built. Returns self for use in `with` statements."""
        Function.set_current_function(self)
        return FunctionContext(self)
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Exits the context of the function, reverting the currently active function to the previous one in the stack."""
        Function.get_back_current_function()
        self.namespace.add_function(self)

    @staticmethod
    def of(id: Identifier) -> "Function":
        """Returns the function with the given identifier, creating it if it does not already exist. This is a convenient method for getting or creating functions without needing to manage their instances directly. The function will be associated with the namespace corresponding to the identifier's namespace, and will be stored in a global registry of functions to ensure that each function is unique based on its identifier.
        """
        if id in Function.fns:
            return Function.fns[id]
        else:
            func = Function(id)
            Function.fns[id] = func
            return func

    def run(self, args: dict | DataStorage | None = None) -> "RunFunction":
        """Returns a `RunFunction` command that executes this function with the given arguments. The arguments can be provided as a dictionary of key-value pairs, or as a `DataStorage` object containing the arguments. If no arguments are provided, the function will be executed without any arguments. This method is a convenient way to create a command that runs the function, and can be used in command sequences or other contexts where commands are needed."""
        from datagen.function.commands.runfunction import RunFunction
        return RunFunction(self, args)
    
class FunctionContext(Function):
    def __new__(cls, f: "Function") -> Self:
        if id in cls.fns:
            return cls.fns[f.id]
        else:
            func = super(Function, cls).__new__(cls)
            cls.fns[f.id] = func
            return func

    def __init__(self, f: "Function"):
        super().__init__(
            f.id
        )
        self.function = f

        self.id = self.function.id
        self.namespace = self.function.namespace
        self.commands = self.function.commands

    def __getitem__[T = Any](
        self, 
        key: tuple[str, type[T] | T] | str
    ) -> FunctionMacroArgument[T]:
        if isinstance(key, tuple):
            key = key[0]
        return FunctionMacroArgument(key) # type: ignore
    
    def arg[T = Any](
        self, 
        key: str, 
        as_: type[T] | T = Any
    ) -> FunctionMacroArgument[T]:
        return self[key, as_]