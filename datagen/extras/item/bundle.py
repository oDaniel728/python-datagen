from typing import Iterable

from datagen.utils.minecraft.collections.items import Items
from datagen.utils.repr.item import Item
from datagen.extras.item.settings.bundleitemsettings import BundleItemSettings


class Bundle(Item[BundleItemSettings]):
    def __init__(self, settings: BundleItemSettings | None = None) -> None:
        super().__init__(
            Items.BUNDLE.id,
            settings or BundleItemSettings()
        )