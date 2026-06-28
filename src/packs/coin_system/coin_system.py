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
from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.levelbasedvalue import LevelBasedValue
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
from packs.coin_system.pack_objectives.coin_healths import COIN_HEALTHS
from packs.coin_system.pack_objectives.roll import ROLL
from packs.coin_system.pack_selectors.glowing_items import NOT_GLOWING_ITEMS
from packs.coin_system.pack_selectors.orbs import EXP_ORB
from packs.coin_system.pack_settings import textsettings

class CoinSystem(Pack, name='csys'):
    def on_prepare(self) -> None:
        return None
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        
        # Enchantments
        ns += BUNDLES, COINS, EMERALDS, DAMAGE, ITEMS
            
        # EntityTags
        COIN_TAG = "coin"
        
        with ns.create_function("load").hook(mc.load) as load:
            
            ~ COIN_HEALTHS
            ~ AGES_SOBJ
            ~ ROLL

        with ns.create_function("ticks/each_coin").hook(mc.tick) as ec:
            SSELF = COIN_HEALTHS.player(TargetSelector.SELF)
            DSELF = EntityData(TargetSelector.SELF)

            with AnonymousFunction() as a1:
                ~ DSELF["CustomName"].set(f"'{a1["Health"]}'")
                ~ DSELF["CustomNameVisible"].set(True)
                tmp += a1
            ~ SSELF.set(Data.get("entity", TargetSelector.SELF, "Health"))

            args = DataStorage(tmp / "a1args")
            ~ args["Health"].set(DSELF["Health"])
            ~ a1.run(args)

        with ns.create_function("tick").hook(mc.tick) as tick:
            ~ Execute() \
                .ASAT(
                    TargetSelector
                        .ALL_ENTITIES
                        .with_settings(
                            TargetSelectorSettings()
                            .with_tag(COIN_TAG)
                        )
                    ) \
                .RUN(ec)
            
        with ns.create_function("ticks/clear_bundles").hook(mc.tick) as clear_bundles:
            ~ Clear(TargetSelector.ALL_PLAYERS, Items.BUNDLE.with_settings(
                BaseItemSettings().with_custom_data({"bundle": True}).with_("bundle_contents", "[]")
            ))

        with ns.create_function("ticks/add_tag_glow").hook(mc.tick) as add_tag_glow:
            with ns.create_function("ticks/inner/add_tag_glow") as inner_add_tag_glow:
                DSELF = EntityData(TargetSelector.SELF)
                SSELF = AGES_SOBJ.player(TargetSelector.SELF)
                ~ SSELF.set(DSELF["Age"].get())
                ~ tag._Tag.add("glow", NOT_GLOWING_ITEMS)

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

        with ns.create_function("ticks/make_items_glow").hook(mc.tick) as make_items_glow:
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

        with ns.create_function("ticks/each_coin_item").hook(mc.tick) as each_coin_item:
            
            with ns.create_function("ticks/inner/each_coin_item") as each_item:
                DSELF = EntityData(TargetSelector.SELF)
                
                SSELF = ROLL.player(TargetSelector.SELF)
                ~ SSELF.set(Random.value(Range(1, 250)))
                
                ~ DSELF["CustomNameVisible"].set(True)
                ~ DSELF["CustomName"].set(
                    DSELF["Item"]["components"]["minecraft:item_name"]
                )
                ~ Execute() \
                    .IF(lambda b: b.score(SSELF, "matches", Range(1, 2))) \
                    .RUN(DSELF["Motion[1]"].set(0.2))
                
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

        with ns.create_function("ticks/each_exp_orb").hook(mc.tick) as each_exp_orb:
            with ns.create_function("ticks/inner/each_exp_orb") as each_orb:
                DSELF = EntityData(TargetSelector.SELF)
                with AnonymousFunction() as a2:
                    ~ DSELF["CustomNameVisible"].set(True)
                    ~ DSELF["CustomName"].set(
                        LiteralText(f"{a2['Value']}", textsettings.RARE)
                    )
                   
                    SSELF = ROLL.player(TargetSelector.SELF)
                    ~ SSELF.set(Random.value(Range(1, 250)))
                    ~ Execute() \
                        .IF(lambda b: b.score(SSELF, "matches", Range(1, 2))) \
                        .RUN(DSELF["Motion"][1].set(0.2))

                    tmp += a2 
                ARGS = DataStorage(tmp / "a2args")
                ~ ARGS["Value"].set(DSELF["Value"].get(1))
                ~ a2.run(ARGS)
                
            ~ Execute() \
                .ASAT(EXP_ORB) \
                .RUN(each_orb)

        with ns.create_function("give/spawn_egg/coin") as spawn_egg_c: 
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

    def on_build(self) -> None:
        return None