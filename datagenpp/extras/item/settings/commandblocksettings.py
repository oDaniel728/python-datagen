from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item

class CommandBlockSettings(Block.Settings):
    def __init__(self, command: Command | str, facing: Block._TDirection, conditional: bool, auto: bool = False) -> None:
        super().__init__()
        self.command = command if isinstance(command, Command) else CustomCommand(command)
        self.facing = facing
        self.conditional = conditional
        self.auto = auto

    def get_block_entity_data(self) -> dict:
        return {"auto": self.auto, "Command": self.command.to_string()}
    
    def get_block_state(self) -> dict:
        return {"facing": self.facing, "conditional": self.conditional}