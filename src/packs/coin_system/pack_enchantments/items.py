from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.text._components import LiteralText
from packs.coin_system.pack_enchantments.common import basic_enchantment


ITEMS = basic_enchantment(
    Namespace.temp() / "items",
    LiteralText("Items"),
    10,
    1,
    (20, 30, 30, 40),
    20,
    ["#minecraft:swords"]
)