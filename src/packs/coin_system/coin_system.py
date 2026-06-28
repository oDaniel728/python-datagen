from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands import tag
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._data.entitydata import EntityData
from datagen.function.commands.clear import Clear
from datagen.function.commands.data import Data
from datagen.function.commands.execute import Execute
from datagen.function.commands.give import Give
from datagen.function.commands.random import Random
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.levelbasedvalue import LevelBasedValue
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagenpp.extras.item.entityspawnegg import EntitySpawnEgg
from datagenpp.extras.item.settings.baseitemsettings import BaseItemSettings
from datagenpp.extras.packs.pack import Pack
from packs.coin_system.pack_enchantments.bundles import BUNDLES
from packs.coin_system.pack_enchantments.coins import COINS
from packs.coin_system.pack_enchantments.damage import DAMAGE
from packs.coin_system.pack_enchantments.emeralds import EMERALDS
from packs.coin_system.pack_enchantments.items import ITEMS
from packs.coin_system.pack_entities.coin import Coin
from packs.coin_system.pack_items.coinbundleitem import CoinBundleItem, ItemBundle
from packs.coin_system.pack_items.coins.feather import FeatherCoin
from packs.coin_system.pack_loot.coinloot import CoinLoot
from packs.coin_system.pack_objectives.ages import AGES_SOBJ
from packs.coin_system.pack_objectives.roll import ROLL
from packs.coin_system.pack_selectors.glowing_items import NOT_GLOWING_ITEMS
from packs.coin_system.pack_selectors.orbs import EXP_ORB
from packs.coin_system.pack_settings import textsettings


class CoinSystem(Pack, name='csys'):
    def on_prepare(self) -> None:
        return None
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        
        ns += BUNDLES, COINS, EMERALDS, DAMAGE, ITEMS
            
        TAG = "coin"
        SCORE: ScoreboardObjective
        with Function(ns / "load") as load:
            
            SCORE = ~ Scoreboard.objective("coin_healths", LiteralText.EMPTY, ObjectiveCriterion.DUMMY)

            ns += load
            mc.load += load

        with Function(ns / "ticks/each_coin") as ec:
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
                BaseItemSettings().with_custom_data({"bundle": True}).with_("bundle_contents", "[]")
            ))

            ns += clear_bundles
            mc.tick += clear_bundles

        with Function(ns / "ticks/add_tag_glow") as add_tag_glow:
            with Function(ns / "ticks/inner/add_tag_glow") as inner_add_tag_glow:
                THIS = EntityData(TargetSelector.SELF)
                SELF = (~ AGES_SOBJ).player(TargetSelector.SELF)
                ~ SELF.set(THIS["Age"].get())
                ~ tag._Tag.add("glow", NOT_GLOWING_ITEMS)

                ns += inner_add_tag_glow
            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_tag("!glow")
                    )
                ) \
                .RUN(inner_add_tag_glow)

            ns += add_tag_glow
            mc.tick += add_tag_glow

        with Function(ns / "ticks/make_items_glow") as make_items_glow:
            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_tag("glow")
                    )
                ) \
                .RUN(
                    EntityData(TargetSelector.SELF)["Glowing"].set(True)
                )

            ns += make_items_glow
            mc.tick += make_items_glow

        with Function(ns / "ticks/each_coin_item") as each_coin_item:
            
            with Function(ns / "ticks/inner/each_coin_item") as each_item:
                THIS = EntityData(TargetSelector.SELF)
                
                SELF = (~ ROLL).player(TargetSelector.SELF)
                ~ SELF.set(Random.value(Range(1, 250)))
                
                ~ THIS["CustomNameVisible"].set(True)
                ~ THIS["CustomName"].set(
                    THIS["Item"]["components"]["minecraft:item_name"]
                )
                ~ Execute() \
                    .IF(lambda b: b.score(SELF, "matches", Range(1, 2))) \
                    .RUN(THIS["Motion[1]"].set(0.2))
                
                ns += each_item 

            ~ Execute() \
                .ASAT(
                    TargetSelector.ALL_ENTITIES
                    .with_settings(
                        TargetSelectorSettings()
                        .with_type(EntityTypes.ITEM)
                        .with_nbt({"Item": {"components": {"minecraft:custom_data": {"show": True}}}})
                    ) 
                ) \
                .RUN(each_item)

            ns += each_coin_item
            mc.tick += each_coin_item

        with Function(ns / "ticks/each_exp_orb") as each_exp_orb:
            with Function(ns / "ticks/inner/each_exp_orb") as each_orb:
                THIS = EntityData(TargetSelector.SELF)
                with AnonymousFunction() as a2:
                    ~ THIS["CustomNameVisible"].set(True)
                    ~ THIS["CustomName"].set(
                        LiteralText(f"{a2['Value']}", textsettings.RARE)
                    )
                   
                    SELF = (~ ROLL).player(TargetSelector.SELF)
                    ~ SELF.set(Random.value(Range(1, 250)))
                    ~ Execute() \
                        .IF(lambda b: b.score(SELF, "matches", Range(1, 2))) \
                        .RUN(THIS["Motion"][1].set(0.2))

                    tmp += a2 
                ARGS = DataStorage(tmp / "a2args")
                ~ ARGS["Value"].set(THIS["Value"].get(1))
                ~ a2.run(ARGS)
                
                ns += each_orb

            ~ Execute() \
                .ASAT(EXP_ORB) \
                .RUN(each_orb)
            
            ns += each_exp_orb
            mc.tick += each_exp_orb

        with Function(ns / "give/spawn_egg/coin") as spawn_egg_c: 
            featherloot = CoinLoot(ns / "coin_tables/coin") \
                .add_coin_with_bonus(
                    FeatherCoin(),
                    Range(1, 3),
                    Range(1, 10),
                    weight=1,
                    unenchanted_chance=0.1,
                    enchanted_chance=LevelBasedValue.linear(0.1, 0.09)
                ) \
                .add_bundle(
                    CoinBundleItem( 
                        FeatherCoin(), 10, LiteralText("Coin Bundle I", textsettings.COMMON), "common"
                    ),
                    unenchanted_chance=0.1,
                    enchanted_chance=LevelBasedValue.lookup([i / 10 for i in range(1, 6)], 0)
                ) \
                .add_bundle(
                    CoinBundleItem(
                        FeatherCoin(), 25, LiteralText("Coin Bundle II", textsettings.UNCOMMON), "uncommon"
                    ),
                    unenchanted_chance=0.05, 
                    enchanted_chance=LevelBasedValue.lookup([max(0, i / 5) for i in range(-4, 7)], 0)
                ) \
                .add_bundle( 
                    ItemBundle(
                        [FeatherCoin().get_stack(25)] * 4, 
                        LiteralText("Coin Bundle III", textsettings.RARE),
                        "rare"
                    ),
                    unenchanted_chance=0.005,
                    enchanted_chance=LevelBasedValue.lookup([max(0, i / 2) for i in range(-8, 3)], 0)
                ) \
                .seal()
            egg = EntitySpawnEgg(Coin(EntityTypes.CHICKEN, featherloot))
            ~ Give(TargetSelector.SELF, egg.get_stack())
            ns += featherloot
            ns += spawn_egg_c

    def on_build(self) -> None:
        return None