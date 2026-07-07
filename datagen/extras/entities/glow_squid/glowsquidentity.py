from datagen.extras.entities.baseentity import BaseEntity
from datagen.extras.entities.mobentity import MobEntity
from datagen.utils.minecraft.collections.entity_types import EntityTypes


class GlowSquidEntity(BaseEntity, MobEntity):
    def __init__(self):
        super().__init__(EntityTypes.GLOW_SQUID)

    def with_dark_ticks_remaining(self, dark_ticks_remaining: int) -> "GlowSquidEntity":
        """
        Countdown of ticks remaining until the glow squid starts glowing.
        Not glowing while positive, glowing when countdown reaches zero.
        """
        self.properties["DarkTicksRemaining"] = dark_ticks_remaining
        return self
