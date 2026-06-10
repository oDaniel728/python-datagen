from datagen.utils.minecraft.collections.items import Items
from datagen.utils.repr.item import Item
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings


class StickFood(Item[BaseItemSettings]):
    def __init__(self):
        super().__init__(
            Items.STICK.id,
            BaseItemSettings()
            .with_food()
        )