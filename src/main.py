from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.bossbar import BossBar
from datagen.function.commands.execute import Execute
from datagen.function.commands.fill import Fill
from datagen.function.commands.give import Give
from datagen.function.commands._return import Return
from datagen.function.commands.ride import Ride
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.commands.setblock import SetBlock
from datagen.function.commands.teleport import Teleport
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.tag.functiontag import FunctionTag
from datagen.tag.tag import Tag
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.blocksettings import BlockSettings
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.repr.position3 import Position3
from datagen.utils.repr.enchantment import Enchantment
from datagen.predicate.predicate import Predicate
from datagen.utils.repr.entitypredicate import EntityPredicate
from datagen.utils.repr.locationpredicate import LocationPredicate
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.damagesourcepredicate import DamageSourcePredicate
from datagen.utils.repr.enchantedchance import EnchantedChance
from datagen.types.util.min import Range
from datagenpp.extras.betterexecute import BetterExecute
from datagenpp.extras.tags.load import Load

def main():

    dp = DataPack("test_datapack", "DataPack created for testing purposes")
    
    ns = Namespace("test_namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    load_tag = Load()

    with Function(ns / "load") as load:
        ~ Say("Hello, world!")
        ~ Return.int(1)

        load_tag.add_value(load)

    with Function(ns / "ride_nearest_cart") as ride_nearest_cart:
        with AnonymousFunction(dp) as lambda1:
            ~ Ride.mount(
                TargetSelector.SELF, 
                TargetSelector.nearest(EntityTypes.MINECART)
            )
            ~ Return.int(1)
        
        with AnonymousFunction(dp) as lambda2:
            ~ Return.int(0)
        
        ~ BetterExecute() \
            .ATAS(TargetSelector.SELF) \
            .CONDITION(
                lambda b: b.entity(
                    TargetSelector.nearest(EntityTypes.MINECART)
                ), 
                Return.function(lambda1),
                Return.function(lambda2)
            )
            
    with Function(ns / "test_ride_nearest_cart") as test_ride_to_nearest_cart:
        with AnonymousFunction(dp) as setup_bossbar:
            _bossbar = BossBar(ns/"test")
            ~ _bossbar.add()
            ~ _bossbar.set("visible", True)
            ~ _bossbar.set("players", TargetSelector.ALL_PLAYERS)
            ~ _bossbar.set("max", 1)
            ~ _bossbar.set("value", 0)
        ~ setup_bossbar.run()
        ~ Return.function(
            AnonymousFunction(dp)
                .add_commands(
                    Execute()
                        .STORE("result", "bossbar", _bossbar, "value")
                        .RUN(Return.function(ride_nearest_cart))
                )
        )

    Predicate.use_namespace(ns)
    # Example predicates and predicate-based logic
    damage_source_predicate = Predicate.damage_source_properties(
        DamageSourcePredicate()
            .with_source_entity(
                EntityPredicate().with_type(EntityType(Identifier.of("minecraft", "player")))
            )
            .with_tag("is_projectile", True)
    )

    enchantment_active_predicate = Predicate.enchantment_active_check(False)

    table_bonus_predicate = Predicate.table_bonus(
        Enchantment(Identifier.of("minecraft", "looting")),
        [0.0, 0.1, 0.25]
    )

    match_tool_predicate = Predicate.match_tool(
        ItemPredicate()
            .with_items(Item(Identifier.of("minecraft", "diamond_sword")))
    )

    random_bonus_predicate = Predicate.random_chance_with_enchanted_bonus(
        0.05,
        EnchantedChance.linear(0.1, 0.02),
        Enchantment(Identifier.of("minecraft", "looting"))
    )

    location_predicate = Predicate.location_check(
        LocationPredicate()
            .with_dimension("minecraft:overworld")
            .with_light(Range.range(10, 15)),
        offset_x=0,
        offset_y=1,
        offset_z=0
    )

    time_predicate = Predicate.time_check(Range.exact(1000), period=24000)

    with Function(ns / "predicate_demo") as predicate_demo:
        ~ Execute() \
            .IF(lambda condition: condition.predicate(damage_source_predicate)) \
            .RUN(Say("Damage source predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(match_tool_predicate)) \
            .RUN(Say("Match tool predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(time_predicate)) \
            .RUN(Say("Time check predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(location_predicate)) \
            .RUN(Say("Location check predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(table_bonus_predicate)) \
            .RUN(Say("Table bonus predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(random_bonus_predicate)) \
            .RUN(Say("Random chance with enchanted bonus predicate matched"))
        ~ Execute() \
            .IF(lambda condition: condition.predicate(enchantment_active_predicate)) \
            .RUN(Say("Enchantment active predicate matched"))

    dp.build()