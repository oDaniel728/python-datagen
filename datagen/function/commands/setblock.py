from typing import Any

from datagen.function.commands.command import Command
from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.snbtserializer import SNBTSerializer


class SetBlock(Command):
    def __init__(self, block_pos: BlockPosition, block: Block[Any]):
        super().__init__()
        self.block_pos = block_pos
        self.block = block

    def __get_str_block(self) -> str:
        # <identifier>[<blockstate>]{<nbt>}
        state = list[str]()
        for k, v in self.block.nbt.get_block_state().items():
            state.append(f"\"{k}\"=\"{v}\"")
        state_str = ",".join(state)
        nbt = list[str]()
        for k, v in self.block.nbt.get_block_entity_data().items():
            nbt.append(f"\"{k}\":{SNBTSerializer.serialize(v)}")
        nbt_str = ",".join(nbt)

        out = str()
        out += ~ self.block.id
        out += f"[{state_str}]" if state_str else ""
        out += f"{{{nbt_str}}}" if nbt_str else ""
        return out

    def to_string(self) -> str:
        return self.auto_macro(f"setblock {self.block_pos} {self.__get_str_block()}".strip())