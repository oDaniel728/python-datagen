from datagen.function.commands.command import Command
from datagen.types.exceptions.preventionexception import PreventionException
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.enchantment import Enchantment


class Enchant(Command):
    def __init__(self, target: TargetSelector, enchantment: Enchantment, level: int):
        super().__init__()
        self.target = target
        self.enchantment = enchantment
        self.level = level

        if (level > enchantment.max_level):
            raise PreventionException(f"Level {level} is greater than the maximum level of enchantment {enchantment.id} ({enchantment.max_level})")
        
        elif (level < 1):
            raise PreventionException(f"Level {level} is less than 1")

    def to_string(self) -> str:
        return f"enchant {self.target.to_string()} {self.enchantment.id} {self.level}"