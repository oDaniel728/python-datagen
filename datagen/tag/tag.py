import json
from pathlib import Path
from typing import Iterable, Self, Type

from datagen.function.function import Function
from datagen.globals import TAGS_PATH
from datagen.utils.obfuscator import Obfuscator
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item
from datagen.utils.simplefile import SimpleFile


class Tag[T]():
    """
    # Tag
    - See https://minecraft.wiki/w/Tag_(Java_Edition)
    ## Summary
    Represents a Minecraft tag, which is a collection of values that can be used to group related items, blocks, entities, or functions together. Each tag has an identifier, a set of values, and a flag indicating whether the tag should replace existing tags with the same identifier or merge with them. The Tag class provides methods for adding and removing values, checking for the presence of values, and converting the tag to a JSON representation that can be saved to a file.
    ## Examples
    - Creating a tag with some values
    ```python
    tag = Tag[str](Identifier.of("pack:example"), ["value1", "value2"], replace=True)
    ```
    - Adding a value to a tag
    ```python
    tag.add_value("value3")
    # or
    tag += "value3"
    ```
    - Removing a value from a tag
    ```python
    tag.remove_value("value2")
    ```
    """
    def __init__(self, id: Identifier, values: Iterable[T], replace: bool = False):
        from datagen.datapack.namespace import Namespace
        self.id = id
        self.namespace = Namespace.get(id)

        self.values = set(values)
        self.replace = replace
        self.type: Type[T] = type(list(values)[0]) if len(values) > 0 else None # type: ignore

    def add_value(self, value: T) -> Self:
        self.values.add(value)
        return self
    
    type _TAddition = T | 'Tag[T]'
    def __iadd__(self, other: "_TAddition | tuple[_TAddition, ...]") -> Self:
        """Adds a value or another tag's values to this tag using the `+=` operator. If the other object is a `Tag`, its values will be merged into this tag's values. If the other object is a single value, it will be added to this tag's values. This operator provides a convenient way to combine tags or add individual values to a tag."""
        if isinstance(other, tuple):
            for item in other:
                self.__iadd__(item)
        else:
            if isinstance(other, Tag):
                self.values.update(other.values)
            else:
                self.values.add(other)
        return self
    
    def remove_value(self, value: T) -> Self:
        self.values.remove(value)
        return self

    def parent(self) -> str:
        if self.type == Function:
            return "function"
        elif self.type == Tag:
            return "tag"
        elif self.type == Item:
            return "item"
        return self.type.__class__.__name__
    
    def has_value(self, value: T) -> bool:
        return value in self.values
    
    def index_of(self, value: T) -> int:
        return list(self.values).index(value)
    
    def get(self, index: int) -> T:
        return list(self.values)[index]
    
    def to_list(self) -> list[T]:
        return list(self.values)

    def __process_values__(self, values: Iterable[T]) -> list[str]:
        processed_values = []
        for value in values:
            if isinstance(value, Function):
                processed_values.append(str(value.id))
            elif isinstance(value, Tag):
                processed_values.append(f"#{value.id}")
            elif isinstance(value, Item):
                processed_values.append(value.id.to_string())
            else:
                processed_values.append(str(value))
        return processed_values

    def to_dict(self) -> dict:
        return {
            "replace": self.replace,
            "values": self.__process_values__(self.values)
        }
    
    def to_string(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    def to_file(self) -> SimpleFile:
        path = Obfuscator.obfuscate_path(self.id.get_namespace(), self.id._path)
        return SimpleFile(Path(TAGS_PATH) / self.parent() / (path.replace(".", "/") + ".json"), self.to_string())

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, exc_type, exc, tb):
        pass