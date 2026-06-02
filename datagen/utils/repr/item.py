from typing import TYPE_CHECKING, Any, Self, Type, overload

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
if TYPE_CHECKING:
    from datagen.utils.repr.itemstack import ItemStack

class __Settings__(ToDict):
    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        return {}

class Item[T: __Settings__]():

    class Settings(__Settings__):
        def __init__(self) -> None:
            super().__init__()

    def __init__(self, id: Identifier, components: T | dict = {}) -> None:
        self.id = id
        self.nbt = components if not isinstance(components, dict) else self.Settings()

    def __get_nbt_dict(self) -> dict:
        if not isinstance(self.nbt, dict):
            return self.nbt.to_dict()
        return self.nbt

    def __str__(self) -> str:
        return f"{~self.id}[{','.join(f'\"{k}\"={v}' for k, v in self.__get_nbt_dict().items())}]"

    def __invert__(self):
        return self.id

    # utils
    @overload
    def get_stack(self, /) -> "ItemStack": ...
    @overload
    def get_stack(self, count: int, /) -> "ItemStack": ...

    def get_stack(self, count: int = 1) -> "ItemStack":
        from datagen.utils.repr.itemstack import ItemStack
        return ItemStack(self, count)

    def copy(self) -> "Item[T]":
        return Item[T](self.id, self.nbt) # type: ignore

    def set_nbt(self, nbt: T) -> Self:
        self.nbt = nbt
        return self
    
    def with_settings[U: Settings](self, setting: U) -> "Item[U]":
        return Item[U](self.id, setting)