from datagen.types.util.min import Range
from datagen.utils.minecraft.collections.entity_types import EntityTypes
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from packs.coin_system.pack_objectives.ages import AGES_SOBJ


GLOWING_ITEMS = TargetSelector.ALL_ENTITIES.with_settings(
    TargetSelectorSettings()
    .with_scores({AGES_SOBJ.name: Range.min(40)})
    .with_type(EntityTypes.ITEM)
    .with_tag("glow")
)
NOT_GLOWING_ITEMS = TargetSelector.ALL_ENTITIES.with_settings(
    TargetSelectorSettings()
    .with_scores({AGES_SOBJ.name: Range.min(40)})
    .with_type(EntityTypes.ITEM)
    .with_tag('!' + "glow")
)