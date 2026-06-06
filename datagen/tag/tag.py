import json
from pathlib import Path
from typing import Iterable, Self, Type

from datagen.function.function import Function
from datagen.globals import TAGS_PATH
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item
from datagen.utils.simplefile import SimpleFile


class Tag[T]():
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
        return SimpleFile(Path(TAGS_PATH) / self.parent() / (self.id._path.replace(".", "/") + ".json"), self.to_string())
