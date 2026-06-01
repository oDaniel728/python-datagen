from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.BlockPosition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.snbtserializer import SNBTSerializer


class SetBlock(Command):
    def __init__(self, block_pos: BlockPosition, block: Identifier, nbt: ToDict | dict):
        self.block_pos = block_pos
        self.block = block
        self.nbt = nbt if isinstance(nbt, dict) else nbt.to_dict()

    def _nbt_to_string(self) -> str:
        return SNBTSerializer.serialize(self.nbt)

    def to_string(self) -> str:
        return self.auto_macro(f"setblock {self.block_pos.to_string()} {self.block} {self._nbt_to_string()}")