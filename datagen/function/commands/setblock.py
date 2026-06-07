from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.snbtserializer import SNBTSerializer


class SetBlock(Command):
    def __init__(self, block_pos: BlockPosition, block: Block):
        super().__init__()
        self.block_pos = block_pos
        self.block = block

    def to_string(self) -> str:
        return self.auto_macro(f"setblock {self.block_pos} {self.block}")