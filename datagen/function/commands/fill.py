from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.BlockPosition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.snbtserializer import SNBTSerializer


class Fill(Command):
    def __init__(self, block_pos1: BlockPosition, block_pos2: BlockPosition, block: Identifier, nbt: ToDict | dict):
        self.block_pos1 = block_pos1
        self.block_pos2 = block_pos2
        self.block = block
        self.nbt = nbt if isinstance(nbt, dict) else nbt.to_dict()

    def _nbt_to_string(self) -> str:
        return SNBTSerializer.serialize(self.nbt)

    def to_string(self) -> str:
        return self.auto_macro(f"fill {self.block_pos1.to_string()} {self.block_pos2.to_string()} {self.block} {self._nbt_to_string()}")