from datagen.extras.packs.pack import Pack
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._components import LiteralText

def register_load(pack: Pack):
    "entry point for the datagen pack"
    with~ Function(pack.ns / "load").hook(pack.mc.load) as load:
        ~ TellRaw(TargetSelector.ALL_PLAYERS, LiteralText("Hello, world!"))
    return load