from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.clear import Clear
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.data import Data
from datagen.function.commands.execute import Execute
from datagen.function.commands.give import Give
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.loot_table.loot_table import LootConditions, LootTable
from datagen.utils.repr.enchantment_provider import EnchantmentProvider
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText, ScoreText
from datagen.utils.repr.levelbasedvalue import LevelBasedValue
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagenpp.extras.item.entityspawnegg import EntitySpawnEgg
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings
from datagenpp.extras.itempack import ItemPack
from datagenpp.extras.packs.pack import Pack
from packs.coin_system.pack_entities.coin import Coin
from packs.coin_system.pack_items.coins.feather import FeatherCoin


class CoinSystem(Pack, name='csys'):
    class LOOT_TABLES():
        ...
    def on_prepare(self) -> None:
        return None

    BUNDLES: EnchantmentProvider
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        BUNDLES = EnchantmentProvider(ns / "bundles")
        BUNDLES \
            .with_description(LiteralText("Bundles")) \
            .with_max_level(10) \
            .with_supported_items("#minecraft:swords") \
            .with_primary_items("#minecraft:swords") \
            .with_weight(5) \
            .with_cost(1, 10, 15, 10) \
            .with_anvil_cost(3) \
            .with_slots("any")
        ns += BUNDLES

        TAG = "coin"
        SCORE: ScoreboardObjective
        with Function(ns / "load") as load:
            
            SCORE = ~ Scoreboard.objective("coin_healths", LiteralText.EMPTY, ObjectiveCriterion.DUMMY)

            ns += load
            mc.load += load

        with Function(ns / "each_coin") as ec:
            SELF = SCORE.player(TargetSelector.SELF)
            THIS = EntityData(TargetSelector.SELF)
            with AnonymousFunction() as a1:
                ~ THIS["CustomName"].set(f"'{a1["Health"]}'")
                ~ THIS["CustomNameVisible"].set(True)
                tmp += a1
            ~ SELF.set(Data.get("entity", TargetSelector.SELF, "Health"))

            args = DataStorage(tmp / "a1args")
            ~ args["Health"].set(THIS["Health"])
            ~ a1.run(args)

            ns += ec

        with Function(ns / "tick") as tick:
            ~ Execute() \
                .ASAT(
                    TargetSelector
                        .ALL_ENTITIES
                        .with_settings(
                            TargetSelectorSettings()
                            .with_tag(TAG)
                        )
                    ) \
                .RUN(ec)
            
            ns += tick
            mc.tick += tick

        with Function(ns / "ticks/clear_bundles") as clear_bundles:
            ~ Clear(TargetSelector.ALL_PLAYERS, Items.BUNDLE.with_settings(
                BaseItemSettings().with_custom_data({"pack": True}).with_("bundle_contents", "[]")
            ))

            ns += clear_bundles
            mc.tick += clear_bundles

        with Function(ns / "give/spawn_egg/coin") as spawn_egg_c:
            loot = (LootTable.builder(ns / "coin_tables/coin")
                .pool((1, 3))
                    .entry(name=FeatherCoin()).weight(1).then()
                .end_pool()
                .pool(1, (2, 3))   
                    .entry(name=ItemPack([FeatherCoin().get_stack(10)]).bundle(
                        BaseItemSettings()
                            .with_rarity("common")
                            .with_item_name(LiteralText("Coin Bundle I"))
                    ))
                        .weight(1)
                    .then() 
                    .condition(lambda b: b.random_chance_with_enchanted_bonus(
                        BUNDLES.id, 0.1, LevelBasedValue.linear(.1, .09)
                    ))
                .end_pool()
            .seal())
            egg = EntitySpawnEgg(Coin(EntityTypes.CAVE_SPIDER, loot))
            ~ Give(TargetSelector.SELF, egg.get_stack())
            ns += loot
            ns += spawn_egg_c

    def on_build(self) -> None:
        return None