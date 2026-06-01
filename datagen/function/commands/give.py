from datagen.function.commands.command import Command
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.itemstack import ItemStack


class Give(Command):
    def __init__(self, target: TargetSelector, stack: ItemStack) -> None:
        super().__init__()
        self.target = target
        self.stack = stack

    def to_string(self) -> str:
        return self.auto_macro(f"give {self.target} {self.stack}")