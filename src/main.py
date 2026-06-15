from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.collections.enchantments import Enchantments
from datagen.utils.minecraft.collections.enchantment_tags import EnchantmentTags
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.enchantment_provider import EnchantmentProvider
from datagen.utils.repr.enchantmenteffects import ValueEffect, EntityEffect
from datagen.utils.repr.levelbasedvalue import LevelBasedValue
from datagen.utils.minecraft.text import Text


def main():
    dp = DataPack("enchantment_demo", "Demonstrating custom enchantments")
    ns = Namespace("demo")
    dp += ns

    # --- Custom enchantment: Thunder ---
    thunder = EnchantmentProvider(Identifier.of("demo:thunder"))
    thunder \
        .with_description(Text.literal("Thunder")) \
        .with_max_level(3) \
        .with_weight(5) \
        .with_supported_items("minecraft:diamond_sword", "minecraft:netherite_sword", "minecraft:iron_axe") \
        .with_primary_items("minecraft:diamond_sword") \
        .with_anvil_cost(3) \
        .with_cost(10, 5, 25, 10) \
        .with_slots("mainhand") \
        .with_exclusive_set(str(Enchantments.SHARPNESS)) \
        .with_value_effect(
            "minecraft:damage",
            ValueEffect.add(LevelBasedValue.linear(2.0, 1.0))
        ) \
        .with_entity_effect(
            "minecraft:post_attack",
            EntityEffect.ignite(LevelBasedValue.linear(2, 1)),
            enchanted="attacker",
            affected="victim"
        )
    ~thunder

    # --- Custom enchantment: Frost Aura ---
    frost = EnchantmentProvider(Identifier.of("demo:frost_aura"))
    frost \
        .with_description(Text.literal("Frost Aura", Text.LiteralTextSettings(color="aqua"))) \
        .with_max_level(2) \
        .with_weight(3) \
        .with_supported_items("minecraft:diamond_chestplate", "minecraft:netherite_chestplate") \
        .with_anvil_cost(4) \
        .with_cost(15, 10, 30, 10) \
        .with_slots("chest") \
        .with_entity_effect(
            "minecraft:post_attack",
            EntityEffect.apply_mob_effect(
                to_apply=["minecraft:slowness"],
                min_duration=LevelBasedValue.linear(2, 1),
                max_duration=LevelBasedValue.linear(4, 2),
                min_amplifier=0,
                max_amplifier=1
            ),
            enchanted="victim",
            affected="victim",
            requirements={
                "condition": "minecraft:random_chance",
                "chance": 0.3
            }
        )
    ~frost

    # --- Using Enchantment in commands ---
    from datagen.function.commands.enchant import Enchant
    from datagen.function.commands.give import Give
    from datagen.function.function import Function
    from datagen.utils.minecraft.targetselector import TargetSelector
    from datagen.utils.minecraft.collections.items import Items

    with Function(ns / "give_sharpness_sword") as f:
        ~ Give(TargetSelector.SELF, Items.DIAMOND_SWORD.get_stack())
        ~ Enchant(TargetSelector.SELF, Enchantments.SHARPNESS, 5)

    dp.build()


main()

#nd