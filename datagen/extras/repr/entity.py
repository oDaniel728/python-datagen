from typing import TYPE_CHECKING

from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.summon import Summon
from datagen.utils.converters import Dictionary
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.entitytype import EntityType
if TYPE_CHECKING:
    from datagen.entitytag import EntityTag
    from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.position3 import Position3


class Entity():
    def __init__(self, type: EntityType, properties: Dictionary.TDictionaryProvider):
        self.type = type
        self.properties = Dictionary.auto(properties)

    def with_settings(self, settings: Dictionary.TDictionaryProvider) -> "Entity":
        return Entity(self.type, self.properties | Dictionary.auto(settings))

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
    
    def give(self, item: "ItemStack") -> Command:
        from datagen.function.commands.give import Give
        return Give(self.target(), item)
    
    def kill(self) -> Command:
        from datagen.function.commands.kill import Kill
        return Kill(self.target())
    
    def add_tag(self, tag: "EntityTag") -> Command:
        return tag.add(self.target())

    def __repr__(self) -> str:
        return f"Entity({self.type}, {self.properties})"