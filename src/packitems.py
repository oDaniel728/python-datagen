from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item
from datagenpp.extras.item.settings.adventure.tool import AdventureToolSettings
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings
from datagenpp.extras.item.settings.toolrule import ToolRule

# Example of a custom item with food settings
class StickFood(Item[BaseItemSettings]):
    # The constructor initializes the item with 
    # the ID of a stick and custom food settings
    def __init__(self):
        super().__init__(
            Items.STICK.id,
            BaseItemSettings()
            .with_food()
        )

class TestTool(Item):
    BLOCKS = [
        Blocks.DIRT,
        Blocks.GRASS_BLOCK,
        Blocks.SAND,
        Blocks.RED_SAND,
        Blocks.GRAVEL,
        Blocks.COARSE_DIRT,
        Blocks.PODZOL
    ]
    def __init__(self) -> None:
        super().__init__(
            Items.WOODEN_SHOVEL.id,
            BaseItemSettings()
            .with_max_damage(32)
            .with_tool(
                ToolRule()
                .add_rule(self.BLOCKS)
                .set_damage_per_block(1)
                .set_default_mining_speed(.3)
            ).get_components() | AdventureToolSettings(
                self.BLOCKS
            )
            .get_components()
        )