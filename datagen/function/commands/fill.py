from typing import Any

from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.snbtserializer import SNBTSerializer


class Fill(Command):
    def __init__(self, block_pos1: BlockPosition, block_pos2: BlockPosition, block: Block[Any]):
        super().__init__()
        self.block_pos1 = block_pos1
        self.block_pos2 = block_pos2
        self.block = block

    def to_string(self) -> str:
        return self.auto_macro(f"fill {self.block_pos1.to_string()} {self.block_pos2.to_string()} {self.block}")