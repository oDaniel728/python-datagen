from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.levelbasedvalue import LevelBasedValue, LevelBasedValues
from packs.coin_system.data.csys.enchantment.common import basic_enchantment


DAMAGE = basic_enchantment(
    Namespace.temp() / "damage",
    LiteralText("Damage"),
    100,
    1,
    (20, 30, 30, 40),
    20,
    ["#minecraft:swords"]
).with_effect("minecraft:damage", *[{
    "effect": {
        "type": "minecraft:add",
        "value": LevelBasedValues.linear(1.0, 5.0).to_dict()
    }
}])