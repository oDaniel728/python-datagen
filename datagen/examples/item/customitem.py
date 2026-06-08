from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands._return import Return
from datagen.function.commands.give import Give
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item


class CustomItemSettings(Item.Settings):
    def __init__(self, custom_name: str) -> None:
        super().__init__()
        self.custom_name = custom_name

    def get_components(self) -> dict:
        return {"custom_name": self.custom_name}
    
class CustomItem(Item[CustomItemSettings]):
    def __init__(self) -> None:
        super().__init__(
            Identifier.of("minecraft", "stone"),
            CustomItemSettings("Custom Stone")
        )

def main():
    dp = DataPack("pack", "")

    ns = Namespace("namespace")
    dp.add_namespace(ns)

    mc = Namespace.minecraft
    dp.add_namespace(mc)

    with Function(ns / "give_custom_item") as func:
        item = CustomItem()
        ~ Return.run(
            Give(TargetSelector.SELF, item.get_stack())
        )

    ns.add_function(func)

