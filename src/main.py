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
from datagen.recipes.recipe import Recipe
from datagen.tag.functiontag import FunctionTag
from datagen.tag.itemtag import ItemTag
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
from datagenpp.extras.item.commandblock import CommandBlock
from datagenpp.extras.item.settings.commandblocksettings import CommandBlockSettings
from datagenpp.extras.recipes.recipeutils import RecipeUtils
from datagenpp.extras.tags.load import Load

def main():

    dp = DataPack("test_datapack", "DataPack created for testing purposes")
    
    ns = Namespace("test_namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    coals = ItemTag(ns / "coals", [Items.COAL, Items.CHARCOAL])
    ns.add_tag(coals)
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
    
    ns.add_recipes(
        *RecipeUtils
            .crafting
            .offer_chain_transformation([
                ([Items.RAW_IRON, Items.COAL], Items.IRON_INGOT.get_stack(1)),
                ([Items.RAW_GOLD, Items.COAL], Items.GOLD_INGOT.get_stack(1)),
                ([Items.RAW_COPPER, Items.COAL], Items.COPPER_INGOT.get_stack(1)),
            ])
        )
    ns.add_recipes(
        RecipeUtils
            .crafting
            .offer_surrounded_core(
                core=coals,
                surrounding=ItemTag(Identifier.of("minecraft:logs_that_burn")),
                result=Items.CHARCOAL.get_stack(8)
            )
    )
    ns.add_recipes(
        Recipe.shapeless(
            ingredients=[*[Items.CHARCOAL] * 8, Items.BLACK_DYE],
            result=Items.COAL.get_stack(8)
        )
    )

    with Function(ns / "put_hello_world") as put_hello_world:
        cmd = CommandBlock(CommandBlockSettings("say hello, world!", "up", False, True))
        ~ SetBlock(RelativeBlockPosition(0, 1, 0), cmd)

    dp.build()