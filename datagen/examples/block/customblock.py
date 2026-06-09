from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands._return import Return
from datagen.function.commands.give import Give
from datagen.function.commands.setblock import SetBlock
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.block import Block


class CustomBlockSettings(Block.Settings):
    def __init__(self) -> None:
        super().__init__()

    def get_block_entity_data(self) -> dict:
        return {}
    
    def get_block_state(self) -> dict:
        return {}
    
    def get_components(self) -> dict:
        return super().get_components() | {
            "custom_name": "Custom Stone"
        }

class CustomBlock(Block[CustomBlockSettings]):
    def __init__(self) -> None:
        super().__init__(
            Identifier.of("minecraft", "stone"),
            CustomBlockSettings()
        )

def main():
    dp = DataPack("pack", "")
    ns = Namespace("namespace")
    dp.add_namespace(ns)

    with Function(ns / "give_custom_block") as func:
        block = CustomBlock()
        ~ Return.run(
            Give(TargetSelector.SELF, block.get_stack())
        )

    with Function(ns / "set_custom_block") as func:
        block = CustomBlock()
        ~ Return.run(
            SetBlock(RelativeBlockPosition(0, -1, 0), block)
        )

    ns.add_function(func)
    dp.build()