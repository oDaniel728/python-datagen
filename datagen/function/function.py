from typing import Self

from datagen.utils.minecraft.identifier import Identifier
from datagen.function.commands.command import Command
from datagen.globals import FUNCTIONS_PATH
from datagen.utils.simplefile import SimpleFile


class Function():
    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace: Namespace = Namespace.get(id)

        self.commands = list[Command]()

    def add_command(self, command: Command) -> Self:
        self.commands.append(command)
        return self

    def get_filepath(self):
        return FUNCTIONS_PATH + self.id._path.replace(".", "/").replace(" ", "_") + ".mcfunction"

    def to_string(self) -> str:
        c = ""
        c += "# " + self.id._path + "\n"
        for command in self.commands:
            c += "\n" + command.to_string()
        return c
    
    def __str__(self) -> str:
        return self.id.__str__()
    
    def to_file(self) -> SimpleFile:
        return SimpleFile(self.get_filepath(), self.to_string())