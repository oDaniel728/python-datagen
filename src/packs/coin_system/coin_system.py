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
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.summon import Summon
from datagen.function.commands.team import Team
from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.levelbasedvalue import LevelBasedValues
from datagen.utils.repr.position3 import Position3
from datagenpp.extras.entityteam import EntityTeam
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
from packs.coin_system.pack_teams.util import make_rarity_team

class CoinSystem(Pack, name='csys'):
    def on_prepare(self) -> None:
        return None
    
    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        
        # Enchantments
        ns += BUNDLES, COINS, EMERALDS, DAMAGE, ITEMS

        # Teams
        BASIC_TEAM: EntityTeam
        COMMON_TEAM: EntityTeam
        UNCOMMON_TEAM: EntityTeam
        RARE_TEAM: EntityTeam
        EPIC_TEAM: EntityTeam
        LEGENDARY_TEAM: EntityTeam
            
        # EntityTags
        COIN_TAG = "coin"
        
        with ns.create_function("load").hook(mc.load) as load:
            
            ~ COIN_HEALTHS
            ~ AGES_SOBJ
            ~ ROLL

            arr, BASIC_TEAM = make_rarity_team("basic")
            ~ arr
            arr, COMMON_TEAM = make_rarity_team("common")
            ~ arr
            arr, UNCOMMON_TEAM = make_rarity_team("uncommon")
            ~ arr
            arr, RARE_TEAM = make_rarity_team("rare")
            ~ arr
            arr, EPIC_TEAM = make_rarity_team("epic")
            ~ arr
            arr, LEGENDARY_TEAM = make_rarity_team("legendary")
            ~ arr
            del arr

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

                with AnonymousFunction() as _:
                    item_name = _['0']
                    count = _['1']
                    id = _['2']
                    rarity = _['3']
                    ~ DSELF["CustomName"].set(f"[{{ \"text\": \"{count}x \" }}, {item_name}]")
                    ~ Team.join(rarity, TargetSelector.SELF)
                    tmp += _

                ARGS = DataStorage(tmp / "_args")
                ~ ARGS.rset({
                    "0": DSELF["Item"]["components"]["minecraft:item_name"],
                    "1": DSELF["Item"]["count"],
                    "2": DSELF["Item"]["id"],
                    "3": DSELF["Item"]["components"]["minecraft:custom_data"]["rarity"]
                })
                ~ _.run(ARGS)
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

        # Entities
        # # Coin 1
        feathercoinloot = CoinLoot(ns / "coin_tables/coin") \
            .add_coin_with_bonus(
                FeatherCoin(),
                Range(1, 3),
                Range(1, 10),
                weight=1,
                unenchanted_chance=0.1,
                enchanted_chance=LevelBasedValues.linear(0.1, 0.09)
            ) \
            .add_bundle(
                CoinBundleItem( 
                    FeatherCoin(), 10, LiteralText("Coin Bundle I", textsettings.COMMON), "common"
                ),
                unenchanted_chance=0.2,
                enchanted_chance=LevelBasedValues.lookup([i / 10 for i in range(1, 6)], 0)
            ) \
            .add_bundle(
                CoinBundleItem(
                    FeatherCoin(), 25, LiteralText("Coin Bundle II", textsettings.UNCOMMON), "uncommon"
                ),
                unenchanted_chance=0.1, 
                enchanted_chance=LevelBasedValues.lookup([max(0, i / 5) for i in range(-4, 7)], 0)
            ) \
            .add_bundle( 
                ItemBundle(
                    [FeatherCoin().get_stack(25)] * 4, 
                    LiteralText("Coin Bundle III", textsettings.RARE),
                    "rare"
                ),
                unenchanted_chance=0.005,
                enchanted_chance=LevelBasedValues.lookup([max(0, i / 2) for i in range(-8, 3)], 0)
            ) \
        .seal()
        ns += feathercoinloot
        feathercoin = Coin(
            EntityTypes.CHICKEN, 
            feathercoinloot
        )

        with ns.create_function("give/spawn_egg/coin") as give_feather_spawn_egg: 
            egg = EntitySpawnEgg(feathercoin)
            ~ Give(TargetSelector.SELF, egg.get_stack())

        with ns.create_function("summon/coins/feather") as summon_feather_coin:
            ~ Summon.entity(feathercoin.type, Position3.auto("~ ~ ~"), feathercoin.nbt())    

        with ns.create_function("utils/run_at_random_position") as run_at_random_position:
            _0 = run_at_random_position.arg("0", int)
            _1 = run_at_random_position.arg("1", int)
            _2 = run_at_random_position.arg("2", int)
            _3 = run_at_random_position.arg("3", int)
            _4 = run_at_random_position.arg("4", int)
            _5 = run_at_random_position.arg("5", int)
            _6 = run_at_random_position.arg("6", str)
            with AnonymousFunction() as a3:
                x = a3['x']
                y = a3['y']
                z = a3['z']
                func = a3['func']
                ~ (
                    Execute()
                        .RUN(RunFunction(func, {'x': x, 'y': y, 'z': z}))
                )
                tmp += a3

            ARGS = DataStorage(tmp / "a3args")
            ~ ARGS.rset({
                "x": Random.value(f"{_0}..{_1}"),
                "y": Random.value(f"{_2}..{_3}"),
                "z": Random.value(f"{_4}..{_5}"),
                "func": _6
            })

            ~ a3.run(ARGS)
        """
        Runs a function at a random position within the specified bounds. 
        The function to run is specified by the 'func' argument.

        Args:
            0 (int): The minimum x-coordinate of the random position.
            1 (int): The maximum x-coordinate of the random position.
            2 (int): The minimum y-coordinate of the random position.
            3 (int): The maximum y-coordinate of the random position.
            4 (int): The minimum z-coordinate of the random position.
            5 (int): The maximum z-coordinate of the random position.
            6 (str): The function to run at the random position.
        """



    def on_build(self) -> None:
        return None