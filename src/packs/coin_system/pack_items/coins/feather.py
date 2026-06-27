from datagen.utils.minecraft.collections.items import Items
from packs.coin_system.pack_items.coinitem import CoinItem


class FeatherCoin(CoinItem):
    def __init__(self) -> None:
        super().__init__(Items.FEATHER.id, "Coin made of feather", 1)