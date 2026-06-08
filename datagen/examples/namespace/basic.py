from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.tag.itemtag import ItemTag
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text

def main():
    # Create a new datapack with the name "pack" and description "a pack"
    dp = DataPack("pack", "a pack")

    # Create a new namespace with the name "pack"
    ns = Namespace("pack")

    # Gets the minecraft namespace for adding resources to it
    mc = Namespace.minecraft

    # Create a new function with the identifier "pack:hello"
    with Function(ns / "hello") as f:
        # Add a command to the function that says "Hello, world!" to all players
        ~ Say("Hello, world!")

    # Add the function to the minecraft namespace's load tag, so it will
    # be executed when the datapack is loaded
    with ItemTag(ns / "coals") as t:
        # Add coal and charcoal to the tag using the `+=` operator, 
        # which allows for adding both individual items and other tags
        t += Items.COAL
        t += Items.CHARCOAL

    # Creates another function that will be added to the tick tag, which 
    # will be executed every game tick
    with Function(ns / "load") as f:
        # Add a command to the function that tells all players "Pack loaded!" 
        # when the datapack is loaded
        ~ TellRaw(
            TargetSelector.ALL_PLAYERS, # @a
            Text.literal("Pack loaded!") # { "text": "Pack loaded!" }
        )
        
        # Add the function to the minecraft namespace's load tag, 
        # so it will be executed when the datapack is loaded
        mc.load += f
        
    dp += ns
    dp.build()