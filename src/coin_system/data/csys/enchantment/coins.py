from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.text._components import LiteralText
from coin_system.data.csys.enchantment.common import basic_enchantment


COINS = basic_enchantment(
    Namespace.temp() / "coins",
    LiteralText("Coins"),
    10,
    1,
    (20, 30, 30, 40),
    20,
    ["#minecraft:swords"]
)