from datagen.advancement.advancement import Advancement
from datagen.advancement.criteria import Criteria
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.advancements import Advancements
from datagen.function.commands.give import Give
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.itempredicate import ItemPredicate
from datagenpp.extras.scripts.scriptbuilder import ScriptBuilder
from packitems import StickFood, TestTool

# EntryPoint of the builder
def main():
    # Datapack building example with custom 
    # item settings and advancements criteria
    with DataPack("pack", "a pack") as dp:
        
        # Creating a namespace for the pack
        with Namespace("pack") as ns:

            # Creating a function that will be 
            # called when the player consumes a stick
            with Function(ns / "on_consume_of_stick") as f:
                ~ Say("You consumed a stick!")

            # Creating an advancement that will be 
            # granted when the player consumes a stick
            ~ ScriptBuilder().on_criteria(
                # The criteria is defined as consuming an 
                # item that matches the predicate of being 
                # a stick
                Criteria.consume_item(
                    ItemPredicate()
                    .with_items(Items.STICK)
                ), 
                f # The function to run when the criteria is met
            )

            # Creating a function that will give the player a 
            # stick with custom food settings
            with Function(ns / "hello") as f:
                ~ Say("Hello, world!")

            # Creating a function that will give the player a 
            # stick with custom food settings
            with Function(ns / "give_stick") as f:
                ~ Give(
                    TargetSelector.SELF,
                    StickFood().get_stack()
                )

            with Function(ns / "give_tool") as f:
                ~ Give(
                    TargetSelector.SELF,
                    TestTool().get_stack()
                )

        # Adding the namespace to the datapack    
        dp.add_namespace(ns)

    # Building the datapack, which will generate the necessary
    dp.build()

#nd