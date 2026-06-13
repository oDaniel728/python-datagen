import abc
import json
from typing import TYPE_CHECKING, Any, Self, Type, overload

from datagen.types.protocols.todict import ToDict
from datagen.utils.minecraft.identifier import Identifier
if TYPE_CHECKING:
    from datagen.utils.repr.itemstack import ItemStack

class __Settings__(ToDict, abc.ABC):
    def __init__(self) -> None:
        pass

    def to_dict(self) -> dict:
        return self.get_components()

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @abc.abstractmethod
    def get_components(self) -> dict: ...

class Item[T: __Settings__]():
    r"""
    # Item \<T\>
    - See https://minecraft.wiki/w/Item
    ## Summary
    Represents an item in Minecraft. An item is defined by its identifier and its NBT data, which can be represented by a settings class that extends `Item.Settings`. The NBT data can also be represented by a dictionary, but using a settings class allows for better type checking and code completion.
    - `<T>` being a class that extends `Item.Settings` and represents the NBT data of the item.
    ## Examples
    - Creating an item with default settings
    ```python
    item = Item(Identifier.of("minecraft:stone"))
    print(item)  # Output: minecraft:stone
    ```
    - Creating an item with custom settings
    ```python
    class CustomItemSettings(Item.Settings):
        def __init__(self, custom_name: str) -> None:
            super().__init__()
            self.custom_name = custom_name

        def get_components(self) -> dict:
            return {"custom_name": self.custom_name}
        
    class CustomItem(Item[CustomItemSettings]):
        def __init__(self) -> None:
            super().__init__(
                Identifier.of("minecraft", "stone"),
                CustomItemSettings("Custom Stone")
            )

    def main():
        dp = DataPack("pack", "")

        ns = Namespace("namespace")
        dp.add_namespace(ns)

        mc = Namespace.minecraft
        dp.add_namespace(mc)

        with Function(ns / "give_custom_item") as func:
            item = CustomItem()
            ~ Return.run(
                Give(TargetSelector.SELF, item.get_stack())
            )

        ns.add_function(func)

        dp.build()
    ```
    """

    instances = dict[Identifier, "Item"]()

    class Settings(__Settings__):
        """
        # Item.Settings
        ## Summary
        Represents the settings for an item, which can be used to define the NBT data of the item. This class should be extended to create custom settings for specific items.

        ## Examples
        - Creating a custom settings class for an item
        ```python
        class CustomItemSettings(Item.Settings):
            def __init__(self, custom_name: str) -> None:
                super().__init__()
                self.custom_name = custom_name

            def get_components(self) -> dict:
                return {"custom_name": self.custom_name}

        #
        ```
        """
        def __init__(self) -> None:
            super().__init__()

    class DefaultSettings(Settings):
        def __init__(self) -> None:
            super().__init__()

        def get_components(self) -> dict:
            return {}
        
    class KWSettings(Settings):
        def __init__(self, **kw):
            super().__init__()
            self.kw = kw

        def get_components(self) -> dict:
            return self.kw

    def __init__(self, id: Identifier, components: T | dict = {}) -> None:
        self.id = id
        self.settings = components if not isinstance(components, dict) else self.KWSettings(**components)
        Item.instances[id] = self

    def __get_nbt_dict(self) -> dict:
        if not isinstance(self.settings, dict):
            return self.settings.to_dict()
        return self.settings

    @staticmethod
    def _remove_nulls(v: Any, depth: int = 0) -> Any:
        # print(depth, v)
        c = lambda vv, n = 0: Item._remove_nulls(vv, depth + n)
        if isinstance(v, dict):
            return { k1: v1 
                for k1, v1 in {
                    k: c(vv, 1)
                    for k, vv in v.items() 
                    if vv is not None
                }.items()
                if not (depth >= 1 and (v1 == [] or v1 == {}))
            }
        if isinstance(v, list):
            return [
                c(vv, 1)
                for vv in v 
                if vv is not None
            ]
        if isinstance(v, Identifier):
            return ~v
        return v

    def __str__(self) -> str:
        nbt_dict: dict = self._remove_nulls(self.__get_nbt_dict())
        print(self._remove_nulls(nbt_dict))
        return f"{~self.id}[{','.join(f'{k}={v}' for k, v in nbt_dict.items())}]" if nbt_dict else f"{~self.id}"

    def __invert__(self):
        return self.id

    # utils
    @overload
    def get_stack(self, /) -> "ItemStack": 
        """
        Returns an `ItemStack` with the default count of 1.

        Returns:
            ItemStack: The `ItemStack` with the default count of 1.
        """
        ...
    @overload
    def get_stack(self, count: int, /) -> "ItemStack": 
        """
        Returns an `ItemStack` with the specified count.

        Args:
            count (int): The number of items in the stack.

        Returns:
            ItemStack: The `ItemStack` with the specified count.
        """
        ...
    def get_stack(self, count: int = 1) -> "ItemStack":
        from datagen.utils.repr.itemstack import ItemStack
        return ItemStack(self, count)

    def copy(self) -> "Item[T]":
        """Creates a copy of the current item.

        Returns:
            Item[T]: A new instance of the item with the same identifier and NBT data.
        """
        return Item[T](self.id, self.settings) # type: ignore

    def set_nbt(self, nbt: T) -> Self:
        self.settings = nbt
        return self
    
    def with_settings[U: Settings](self, setting: U) -> "Item[U]":
        """Returns a new `Item` instance with the same identifier but with the provided settings.
        
        Args:
            setting (U): The settings to be applied to the new `Item` instance.
        
        Returns:
            Item[U]: A new instance of the item with the same identifier but with the provided settings.
        """
        return Item[U](self.id, setting)
    
    def to_dict(self) -> dict:
        return self.settings.get_components()