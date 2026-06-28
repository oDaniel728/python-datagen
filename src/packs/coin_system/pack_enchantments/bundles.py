from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.enchantment_provider import EnchantmentProvider
from packs.coin_system.pack_enchantments.common import basic_enchantment

BUNDLES = basic_enchantment(
    Namespace.temp() / "bundles",
    LiteralText("Bundles"),
    10,
    1,
    (20, 30, 30, 40),
    20,
    ["#minecraft:swords"]
)