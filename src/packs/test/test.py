from datagen.datapack.namespace import Namespace
from datagen.function.commands.say import Say
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._components import LiteralText
from packs.pack import Pack

class TestPack(Pack, name="testpack"):

    def on_prepare(self) -> None:
        self.logger.info('Preparing TestPack...')

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        self.logger.info('Registering namespaces for TestPack...')

        with~ Function(ns / "load") as func:
            ~ TellRaw(
                TargetSelector.ALL_PLAYERS,
                LiteralText("TestPack loaded successfully!")
            )
        
        mc.load += func

    def on_build(self) -> None:
        self.logger.info('Building TestPack...')