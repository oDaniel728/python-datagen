from typing import overload

from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.damage import DamageType


class Damage(Command):

    @overload
    def __init__(self, target: TargetSelector, amount: int, /): ...
    @overload
    def __init__(self, target: TargetSelector, amount: int, damage_type: DamageType, /): ...

    def __init__(self, *args):
        target, amount = args[0], args[1]
        damage_type = args[2] if len(args) > 2 else None

        super().__init__()
        self.target: TargetSelector = target
        self.amount: int = amount
        self.damage_type: DamageType | None = damage_type

    def to_string(self) -> str:
        if self.damage_type is not None:
            return f"damage {self.target} {self.amount} {self.damage_type.get()}"
        else:
            return f"damage {self.target} {self.amount}"