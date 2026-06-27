from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.data import Data
from datagen.function.commands.execute import Execute
from datagen.function.commands.give import Give
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.loot_table.loot_table import LootTable
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText, ScoreText
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagenpp.extras.item.entityspawnegg import EntitySpawnEgg
from datagenpp.extras.itempack import ItemPack
from datagenpp.extras.packs.pack import Pack
from packs.coin_system.pack_entities.coin import Coin
from packs.coin_system.pack_items.coins.feather import FeatherCoin


class CoinSystem(Pack, name='csys'):
    class LOOT_TABLES():
        ...
    def on_prepare(self) -> None:
        return None
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
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

        with Function(ns / "give/spawn_egg/coin") as spawn_egg_c:
            loot = (LootTable.builder(ns / "coin_tables/coin")
                .pool((1, 3))
                    .entry(name=FeatherCoin()).weight(1).then()
                .end_pool()
                .pool(1)
                    .entry(name=ItemPack([FeatherCoin().get_stack(10)]).bundle()).weight(1).then()
                    .condition(lambda b: b.random_chance(0.5))
                .end_pool() 
            .seal())
            egg = EntitySpawnEgg(Coin(EntityTypes.CAVE_SPIDER, loot))
            ~ Give(TargetSelector.SELF, egg.get_stack())
            ns += loot
            ns += spawn_egg_c

    def on_build(self) -> None:
        return None