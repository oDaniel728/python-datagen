from typing import Self

from datagen.types.util.holder import Holder
from datagen.utils.converters import IdentifierConverter
from datagen.utils.minecraft.identifier import Identifier
from datagen.types.util.reprs import *

class EntityAttributeModifier():
    _TOperation = Literal["add_value", "add_multiplied_base", "add_multiplied_total"]
    def __init__(
        self,
        amount: double,
        id: Identifier | Holder[Identifier],
        operation: _TOperation
    ) -> None:
        self.amount = amount
        self.id = IdentifierConverter.auto(id)
        self.operation = operation
    
    def with_amount(self, amount: double) -> "EntityAttributeModifier":
        self.amount = amount
        return self
    
    def with_id(self, id: Identifier | Holder[Identifier]) -> "EntityAttributeModifier":
        self.id = IdentifierConverter.auto(id)
        return self
    
    def with_operation(self, operation: _TOperation) -> "EntityAttributeModifier":
        self.operation = operation
        return self

class EntityAttribute():
    def __init__(
        self,
        id: str,
        base: double,
        modifiers: list[EntityAttributeModifier] = []
    ) -> None:
        self.id = id
        self.base = base
        self.modifiers = modifiers

    def with_id(self, id: str) -> "Self":
        self.id = id
        return self
    
    def with_base(self, base: double) -> "Self":
        self.base = base
        return self
    
    def with_modifiers(self, modifiers: list[EntityAttributeModifier]) -> "Self":
        self.modifiers = modifiers
        return self
    
    def add_modifier(self, modifier: EntityAttributeModifier) -> "Self":
        self.modifiers.append(modifier)
        return self