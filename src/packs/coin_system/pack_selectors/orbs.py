from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings


EXP_ORB = TargetSelector.ALL_ENTITIES.with_settings(
    TargetSelectorSettings()
        .with_type("minecraft:experience_orb")
)