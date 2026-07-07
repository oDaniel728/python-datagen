from datagen.extras.entities.display.textdisplayentity import TextDisplayEntity
from datagen.extras.packs.pack import Pack
from datagen.extras.raycaster import RayCaster
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.kill import Kill
from datagen.function.commands.particle import Particle
from datagen.function.commands.teleport import Teleport
from datagen.function.function import Function
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.collections.particle_types import ParticleTypes
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.repr.position3 import Position3


def register_other(pack: Pack):
    HERE = Position3.auto("~ ~ ~")
    ZERO = Position3(0, 0, 0)
    with~ Function(pack.ns / "kill_zombie") as f:
        ~ RayCaster.on_target_hit(
            TargetSelector.ALL_ENTITIES.with_settings(
                TargetSelectorSettings()
                .with_type(EntityTypes.ZOMBIE)
                .do_nearest()
            ),
            CommandArray([Kill(TargetSelector.SELF)]),
            CommandArray([Particle(ParticleTypes.FLAME, HERE, ZERO, 1, 0)]),
        )
    with~ Function(pack.ns / "get_item") as f:
        NEAREST_ITEM = TargetSelector.ALL_ENTITIES.with_settings(
            TargetSelectorSettings()
            .with_type(EntityTypes.ITEM)
            .do_nearest()
        )
        ~ Teleport.look_at_entity(NEAREST_ITEM)
        ~ RayCaster.on_target_hit(
            NEAREST_ITEM,
            CommandArray([Teleport("$(source)")]).to_function(),
            CommandArray([Particle(ParticleTypes.FLAME, HERE, ZERO, 1, 0)]),
        )

    with~ Function(pack.ns / "test") as f:
        ~ (
            TextDisplayEntity()
            .with_text(LiteralText("Hello, world!"))
            .with_tags(["test_tag"])
        ).summon()