from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagenpp.extras.item.settings.commandblocksettings import CommandBlockSettings


class ChainCommandBlock(Block[CommandBlockSettings]):
    def __init__(self, settings: CommandBlockSettings) -> None:
        super().__init__(Blocks.CHAIN_COMMAND_BLOCK.id)
        self.nbt = settings