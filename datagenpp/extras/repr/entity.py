from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.summon import Summon
from datagen.utils.converters import Dictionary
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.position3 import Position3
from datagen.utils.snbtserializer import SNBTSerializer


class Entity():
    def __init__(self, type: EntityType, properties: Dictionary.TDictionaryProvider):
        self.type = type
        self.properties = Dictionary.auto(properties)

    def summon(self, at: Position3 = RelativePlayerPosition(0, 0, 0)) -> CustomCommand:
        return Summon.entity(self.type, at, self.properties)
    
    def target(self, settings: TargetSelectorSettings | None = None) -> TargetSelector:
        if settings is None: settings = TargetSelectorSettings()
        else: settings = settings.copy()
        return TargetSelector.ALL_ENTITIES.with_settings(
            settings
            .with_type(self.type)
            .with_nbt(self.properties)
        )
    
    def nbt(self) -> dict:
        return self.properties | {"id": self.type.id}