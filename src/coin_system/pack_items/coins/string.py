from datagen.utils.minecraft.collections.items import Items
from coin_system.pack_items.coinitem import CoinItem


class StringCoin(CoinItem):
    def __init__(self) -> None:
        super().__init__(Items.STRING.id, "String", "basic", "Coin made of string", 10)