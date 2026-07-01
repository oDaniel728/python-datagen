from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings
from datagenpp.extras.item.settings.bundleitemsettings import BundleItemSettings
from packs.coin_system.pack_items.coinitem import CoinItem

class ItemBundle(Item):
    def __init__(self, items: list[ItemStack], name: BaseText = LiteralText("Bundle"), rarity: BaseItemSettings._TRarity = "common") -> None:
        bundle_settings = BundleItemSettings().with_bundle_contents(items)
        item_settings = BaseItemSettings().with_item_name(name).with_rarity(rarity).with_custom_data({"bundle": True, "show": True, "rarity": rarity}).with_fire_resistant()
        super().__init__(Items.BUNDLE.id, ~bundle_settings | ~item_settings)
class CoinBundleItem(Item):
    def __init__(self, coin: CoinItem, amount: int, name: BaseText = LiteralText("Bundle"), rarity: BaseItemSettings._TRarity = "common") -> None:
        bundle_settings = BundleItemSettings().with_bundle_contents([coin.get_stack(amount)])
        item_settings = BaseItemSettings().with_item_name(name).with_rarity(rarity).with_custom_data({"bundle": True, "show": True, "rarity": rarity}).with_fire_resistant()
        super().__init__(Items.BUNDLE.id, ~bundle_settings | ~item_settings)