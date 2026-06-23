from datagen.datapack.namespace import Namespace
from datagen.function.commands.execute import Execute
from datagen.function.commands.say import Say
from datagen.function.commands.summon import Summon
from datagen.function.commands.tellraw import TellRaw
from datagen.function.function import Function
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagenpp.extras.repr._entitysettings.mobentitysettings import MobEntitySettings
from datagenpp.extras.repr.entity import Entity
from datagenpp.extras.repr.entitysettings import EntitySettings
from packs.pack import Pack

PIGGO = Entity(
    EntityTypes.PIG, 
    MobEntitySettings()
    .with_custom_name("Piggo")
)

def PiggoTargetSelectorSettings() -> TargetSelector:
    return PIGGO.target(
        TargetSelectorSettings()
        .do_nearest().do_first()
    )

class TestPack(Pack, name="testpack"):

    def on_prepare(self) -> None:
        self.logger.info('Preparing TestPack...')

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        self.logger.info('Registering namespaces for TestPack...')

        with~ Function(ns / "load") as load:
            ~ TellRaw(
                TargetSelector.ALL_PLAYERS,
                LiteralText("TestPack loaded successfully!")
            )
        
        with~ Function(ns / "get_piggo") as get_piggo:
            ~ Say("Looking for Piggo...")
            with~ Function(tmp / "when_piggo_found") as when_piggo_found:
                ~ Say("Piggo found!")
            with~ Function(tmp / "when_piggo_not_found") as when_piggo_not_found:
                ~ Say("Piggo not found!")
            ~ (
                Execute()
                .IFELSE(
                    lambda b: b.entity(PiggoTargetSelectorSettings()), 
                    when_piggo_found, 
                    when_piggo_not_found
                )
            )

        with~ Function(ns / "summon_piggo") as summon_piggo:
            ~ Say("Summoning Piggo...")
            ~ (
                PIGGO
                    .with_settings(
                        MobEntitySettings()
                        .with_health(1)
                    )
                    .summon(RelativePlayerPosition(0, 0, 0))
            )
        
        mc.load += load

    def on_build(self) -> None:
        self.logger.info('Building TestPack...')