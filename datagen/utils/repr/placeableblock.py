from datagen.function.commands.setblock import SetBlock
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block


class PlaceableBlock[S: Block.Settings](Block[S]):
    def __init__(self, id: Identifier, nbt: S | dict = {}, pos: BlockPosition = BlockPosition(0, 0, 0)) -> None:
        super().__init__(id, nbt)
        self.pos = pos

    def place(self) -> SetBlock:
        return SetBlock(self.pos, self) # type: ignore