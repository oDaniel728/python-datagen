from datagen.extras.color import Color
from datagen.extras.complex.complexitem import ComplexItem
from datagen.extras.entities.areaeffectcloud.areaeffectcloud import AreaEffectCloudEntity
from datagen.extras.entities.areaeffectcloud.potiontypes import PotionTypes
from datagen.extras.entities.villager.tradeoffer import VillagerTradeOffer
from datagen.extras.entities.villager.villager import VillagerEntity
from datagen.extras.packs.pack import Pack
from datagen.extras.utils.commandchain import CommandChain
from datagen.function.commands.kill import Kill
from datagen.function.commands.say import Say
from datagen.function.commands.summon import Summon
from datagen.function.function import Function
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.collections.items import Items
from datagen.utils.minecraft.collections.particle_types import ParticleTypes
from datagen.utils.minecraft.collections.status_effects import StatusEffects
from datagen.utils.minecraft.collections.villager_professions import VillagerProfessions
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector


def register_test(pack: Pack) -> None:
    
    with~ Function(pack.ns / "test/command_chain") as test_command_chain:
        with CommandChain() as chain:
            ~ Say("Hello, world!")
            ~ Say("This is a command chain!")
            ~ Summon.item(Items.DIAMOND.get_stack(), RelativePlayerPosition(0, 0, 0), {"PickupDelay": 0})
        ~ chain.entity().summon(RelativePlayerPosition(0, 0, 0))

    OP_VILLAGER = VillagerEntity().add_offer(
        VillagerTradeOffer()
            .with_buy(Items.DIRT.get_stack(1))
            .with_sell(Items.DIAMOND.get_stack(64))
            .with_max_uses(-1)
    ).with_villager_profession(VillagerProfessions.FARMER).with_villager_level(5)
    with~ Function(pack.ns / "test/villager") as test_villager:
        ~ OP_VILLAGER.summon()

    with~ Function(pack.ns / "test/area_effect_cloud") as test_area_effect_cloud:
        E = AreaEffectCloudEntity()
        E = (
            E.with_particle(ParticleTypes.FLAME)
            .with_radius(5)
            .with_radius_per_tick(-0.1)
            .with_duration(100)
            .with_duration_on_use(-10)
            .with_potion_contents(PotionTypes.WATER, Color.from_hex("#ff0000"), [
                StatusEffects.LUCK.apply(100, 1).with_show_particles(False)
            ])
        )
        ~ E.summon()

    with~ Function(pack.ns / "test/complex_item") as test_complex_item:
        complex_item = ComplexItem(
            pack.ns / "test_complex_item",
            Blocks.STONE.id,
            {
                "custom_data": {
                    "foo": "bar",
                    "baz": 123,
                }
            }
        )
        ~ complex_item.give(TargetSelector.NEAREST_PLAYER, 1)

    with~ Function(pack.ns / "test/complex_item_on_ground") as test_complex_item_on_ground:
        ~ Kill(complex_item.get_on_ground_target())