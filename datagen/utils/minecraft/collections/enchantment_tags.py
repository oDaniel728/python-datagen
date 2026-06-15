from datagen.utils.minecraft.identifier import Identifier
from datagen.tag.enchantmenttag import EnchantmentTag


class EnchantmentTags():
    CURSE = EnchantmentTag(Identifier.of('minecraft:curse'))
    DOUBLE_TRADE_PRICE = EnchantmentTag(Identifier.of('minecraft:double_trade_price'))
    IN_ENCHANTING_TABLE = EnchantmentTag(Identifier.of('minecraft:in_enchanting_table'))
    NON_TREASURE = EnchantmentTag(Identifier.of('minecraft:non_treasure'))
    ON_MOB_SPAWN_EQUIPMENT = EnchantmentTag(Identifier.of('minecraft:on_mob_spawn_equipment'))
    ON_RANDOM_LOOT = EnchantmentTag(Identifier.of('minecraft:on_random_loot'))
    ON_TRADED_EQUIPMENT = EnchantmentTag(Identifier.of('minecraft:on_traded_equipment'))
    PREVENTS_BEE_SPAWNS_WHEN_MINING = EnchantmentTag(Identifier.of('minecraft:prevents_bee_spawns_when_mining'))
    SMASHER = EnchantmentTag(Identifier.of('minecraft:smasher'))
    TOOLTIP_ORDER = EnchantmentTag(Identifier.of('minecraft:tooltip_order'))
    TREASURE = EnchantmentTag(Identifier.of('minecraft:treasure'))
    EXCLUSIVE_SET_ARMOR = EnchantmentTag(Identifier.of('minecraft:exclusive_set/armor'))
    EXCLUSIVE_SET_BOOTS = EnchantmentTag(Identifier.of('minecraft:exclusive_set/boots'))
    EXCLUSIVE_SET_BOW = EnchantmentTag(Identifier.of('minecraft:exclusive_set/bow'))
    EXCLUSIVE_SET_CROSSBOW = EnchantmentTag(Identifier.of('minecraft:exclusive_set/crossbow'))
    EXCLUSIVE_SET_MINING = EnchantmentTag(Identifier.of('minecraft:exclusive_set/mining'))
    EXCLUSIVE_SET_RIPTIDE = EnchantmentTag(Identifier.of('minecraft:exclusive_set/riptide'))
