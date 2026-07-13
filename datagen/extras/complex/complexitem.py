from datagen.function.commands.clear import Clear
from datagen.function.commands.command import Command
from datagen.function.commands.give import Give
from datagen.function.commands.summon import Summon
from datagen.types.protocols.todict import ToDict
from datagen.utils.converters import Dictionary
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.relativeplayerposition import RelativePlayerPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.item import Item
from datagen.utils.repr.position3 import Position3

class ComplexItem(Item):
    Instances = dict[Identifier, "ComplexItem"]()
    def __init__(self, id: Identifier, base: Identifier, components: ToDict | dict = {}) -> None:
        super().__init__(base, Dictionary.auto(components))
        self.cid = id
        self.settings: dict = Dictionary.auto(components)
        self.settings.setdefault("custom_data", {})["__cid"] = self.cid
        ComplexItem.Instances[self.cid] = self

    def __repr__(self) -> str:
        return f"ComplexItem({self.id}, {self.settings})"
    
    def give(self, to: TargetSelector, quantity: int = 1) -> Command:
        return Give(to, self.get_stack(quantity))
    
    def take(self, from_: TargetSelector, quantity: int | None = None) -> Command:
        if quantity is not None:
            return Clear(from_, self.get_stack(quantity))
        return Clear(from_)
    
    def spawn(self, quantity: int = 1, pos: Position3 = RelativePlayerPosition(0, 0, 0)) -> Command:
        return Summon.item(self.get_stack(quantity), pos)
    
    def get_on_ground_target(self) -> TargetSelector:
        return TargetSelector.ALL_ENTITIES.with_settings(
            TargetSelectorSettings()
                .with_nbt({"Item": {"components": {"minecraft:custom_data": {"__cid": self.cid}}}})
        )
    
    def get_holding_target(self) -> TargetSelector:
        return TargetSelector.ALL_ENTITIES.with_settings(
            TargetSelectorSettings()
                .with_nbt({"SelectedItem": {"components": {"minecraft:custom_data": {"__cid": self.cid}}}})
        )