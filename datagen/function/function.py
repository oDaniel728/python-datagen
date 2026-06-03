from typing import Self

from datagen.utils.minecraft.identifier import Identifier
from datagen.function.commands.command import Command
from datagen.globals import FUNCTIONS_PATH, DatagenConfig
from datagen.utils.simplefile import SimpleFile


class Function():
    __current_function: Function | None = None
    __funcs = dict[Identifier, "Self"]()
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
        indent = " " * DatagenConfig.config["builderSettings"]["indentation"]
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
        Function.__current_function = self
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        Function.__current_function = None
        self.namespace.add_function(self)

    @staticmethod
    def get(id: Identifier) -> "Function":
        if id in Function.__funcs:
            return Function.__funcs[id]
        else:
            func = Function(id)
            Function.__funcs[id] = func
            return func