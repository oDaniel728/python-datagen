from datagen.utils.minecraft.collections.items import Items
from datagen.utils.repr.item import Item
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings

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