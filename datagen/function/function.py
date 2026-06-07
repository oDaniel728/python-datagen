from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.utils.minecraft.identifier import Identifier
from datagen.function.commands.command import Command
from datagen.globals import FUNCTIONS_PATH, DatagenConfig
from datagen.utils.simplefile import SimpleFile


class Function():
    __current_function: Function | None = None
    __functions = list["Function"]()

    @staticmethod
    def get_current_function() -> Function | None:
        return Function.__current_function
    
    @staticmethod
    def set_current_function(func: Function | None):
        Function.__current_function = func
        if func:
            Function.__functions.append(func)

    @staticmethod
    def get_back_current_function() -> Function | None:
        # undoes the current function
        # before: [A, B, C] with current C
        # after: [A, B] with current B
        if Function.__current_function is not None:
            func = Function.__current_function
            Function.__current_function = None
            if func in Function.__functions:
                Function.__functions.remove(func)
            Function.__current_function = Function.__functions[-1] \
                if len(Function.__functions) > 0 \
                else None
            return func
        else:
            return None

    __funcs = dict[Identifier, "Self"]()

    def __new__(cls, id: Identifier) -> Self:
        if id in cls.__funcs:
            return cls.__funcs[id]
        else:
            func = super(Function, cls).__new__(cls)
            cls.__funcs[id] = func
            return func

    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.get(id)

        self.commands = list[Command]()

    def __hash__(self) -> int:
        return hash(self.id)

    def add_command(self, command: Command) -> Self:
        self.commands.append(command)
        return self
    
    def add_commands(self, *commands: Command) -> Self:
        for command in commands:
            self.add_command(command)
        return self

    def get_filepath(self):
        return FUNCTIONS_PATH + self.id._path.replace(".", "/").replace(" ", "_") + ".mcfunction"

    def to_string(self) -> str:
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
        return SimpleFile(self.get_filepath(), self.to_string())
    
    def __iadd__(self, command: Command) -> Self:
        return self.add_command(command)
    
    def __enter__(self) -> Self:
        Function.set_current_function(self)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        Function.get_back_current_function()
        self.namespace.add_function(self)

    @staticmethod
    def of(id: Identifier) -> "Function":
        if id in Function.__funcs:
            return Function.__funcs[id]
        else:
            func = Function(id)
            Function.__funcs[id] = func
            return func

    def run(self, args: dict | DataStorage | None = None) -> "RunFunction":
        from datagen.function.commands.runfunction import RunFunction
        return RunFunction(self, args)