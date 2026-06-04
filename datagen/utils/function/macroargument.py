from datagen.function.commands.command import Command
from datagen.types.protocols.mapper import Mapper
from datagen.types.protocols.tostring import ToString


class MacroArgument(ToString):
    def __init__(self, name: str):
        self.name = name

    def to_string(self) -> str:
        return f"${self.name}"