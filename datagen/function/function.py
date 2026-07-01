from typing import TYPE_CHECKING, Any, Self


from datagen.function.functionmacroargument import FunctionMacroArgument

if TYPE_CHECKING:
    from datagen.tag.functiontag import FunctionTag
    from datagen.datapack.namespace import Namespace
    from datagen.function.commands._data.entitydata import EntityData, BlockEntityData
    from datagen.function.commands.commandarray import CommandArray
    from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.utils.minecraft.identifier import Identifier
from datagen.function.commands.command import Command
from datagen.globals import FUNCTIONS_PATH, DatagenConfig
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.simplefile import SimpleFile


class Function[**P]():
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

    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.temp()

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
        path = Obfuscator.obfuscate_path(self.id.get_namespace(), self.id._path, "identifiers.functions")
        return FUNCTIONS_PATH + path.replace(".", "/").replace(" ", "_") + ".mcfunction"

    def to_string(self) -> str:
        """Converts the function to a string in the format of a Minecraft function file, with proper indentation and formatting."""
        lines: list[str] = []
        lines.append("# " + Obfuscator.obfuscate_path(self.id.get_namespace(), self.id._path, "identifiers.functions"))
        indent = " " * DatagenConfig.config["builderSettings"]["indent"]
        for command in self.commands:
            cmd_str = str(command)
            # remove only leading newlines to avoid accidental empty first line
            cmd_str = cmd_str.lstrip("\n")
            for line in cmd_str.splitlines():
                if line.strip() == "":
                    lines.append("")
                elif line.lstrip().startswith(("#", "$")):
                    # keep comment and macro lines unindented
                    lines.append(line.lstrip())
                else:
                    # normalize existing leading whitespace and indent command lines
                    lines.append(indent + line.lstrip())
        
        _has_comments = DatagenConfig.config["builderSettings"]["comment"]
        if not _has_comments:
            # remove comment lines if comments are disabled
            lines = [line for line in lines if not line.strip().startswith("#")]
            # remove indentation
            lines = [line.lstrip() for line in lines]
        if not DatagenConfig.config["builderSettings"].get("allowEmptyLines", True):
            lines = [line for line in lines if line.strip() != ""]
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.id.__str__()
    
    def to_file(self) -> SimpleFile:
        """Converts the function to a `SimpleFile` object, which can be used to write the function to disk. The file path is determined by the function's identifier and the configured functions path, and the content is generated by the `to_string` method."""
        return SimpleFile(self.get_filepath(), self.to_string())
    
    type _TAddition = "Command | CommandArray"
    def __iadd__(self, command: "_TAddition | tuple[_TAddition, ...]") -> Self:
        """Adds a command to the function using the `+=` operator."""
        from datagen.function.commands.commandarray import CommandArray
        if isinstance(command, tuple):
            for cmd in command:
                self += (cmd)
        else:
            if isinstance(command, CommandArray):
                for cmd in command:
                    self.add_command(cmd)
            else:
                self.add_command(command)
        return self
    
    def __enter__(self) -> "FunctionContext":
        """Enters the context of the function, setting it as the currently active function being built. Returns self for use in `with` statements."""
        Function.set_current_function(self)
        return FunctionContext(self)
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Exits the context of the function, reverting the currently active function to the previous one in the stack."""
        Function.get_back_current_function()
        # self.namespace.add_function(self)

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

    def run(self, args: "dict | DataStorage | EntityData | BlockEntityData | None" = None) -> "CommandArray":
        """Returns a `RunFunction` command that executes this function with the given arguments. The arguments can be provided as a dictionary of key-value pairs, or as a `DataStorage` object containing the arguments. If no arguments are provided, the function will be executed without any arguments. This method is a convenient way to create a command that runs the function, and can be used in command sequences or other contexts where commands are needed."""
        from datagen.function.commands.runfunction import RunFunction
        from datagen.function.commands.commandarray import CommandArray
        from datagen.datapack.namespace import Namespace
        arr = CommandArray([])
        if isinstance(args, dict):
            _args = DataStorage(Namespace.temp() / "__args")
            arr += _args.rset(args)
            arr += RunFunction(self, _args)
        else:
            arr += RunFunction(self, args)
        return arr
    
    def __invert__(self) -> "Self":
        """Returns the function itself, but with the `~` operator. This is a convenient syntax for quickly creating a function instance without needing to call the constructor directly, and can be used in contexts where a function instance is needed but the identifier is already known."""
        from datagen.datapack.datapack import DataPack
        from datagen.datapack.namespace import Namespace
        ns_name = self.id.get_namespace()
        ns = None
        dp = DataPack.get_current_datapack()
        for n in dp.namespaces:
            if n.name == ns_name:
                ns = n
                break
        if ns is None:
            ns = Namespace.temp()
        ns += self
        return self

    def __call__(self, *a: P.args, **k: P.kwargs) -> "CommandArray":
        """Allows the function to be called like a regular Python function, returning a `RunFunction` command that executes this function with the given arguments. The arguments can be provided as positional or keyword arguments, and will be passed to the `run` method to create the appropriate command. This syntax is a convenient way to create a command that runs the function with specific arguments, and can be used in command sequences or other contexts where commands are needed."""
        args = k | {str(i): ag for i, ag in enumerate(a)}
        return self.run(args)
    
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

    def hook(self, at: "Namespace | FunctionTag") -> Self:
        """Hooks the function into the given namespace or function tag, adding it to their list of functions. This is a convenient way to associate a function with a specific namespace or function tag, and can be used to organize functions within a datapack or other context where namespaces and function tags are used."""
        from datagen.datapack.namespace import Namespace
        from datagen.tag.functiontag import FunctionTag
        if isinstance(at, FunctionTag):
            at += self
            return self
        elif isinstance(at, Namespace):
            at += self
            return self
        else:
            raise TypeError(f"Expected Namespace or FunctionTag, got {type(at)}")
    
class FunctionContext(Function):
    def __new__(cls, f: "Function") -> Self:
        if isinstance(f, Identifier):
            f = Function.of(f)
        if f.id in cls.fns:
            return cls.fns[f.id]
        else:
            func = super(Function, cls).__new__(cls)
            cls.fns[f.id] = func
            return func

    def __init__(self, f: "Function"):
        if isinstance(f, Identifier):
            f = Function.of(f)
        super().__init__(
            f.id
        )
        self.function = f

        self.id = self.function.id
        self.namespace = self.function.namespace
        self.commands = self.function.commands