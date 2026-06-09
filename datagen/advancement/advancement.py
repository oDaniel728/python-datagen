import json
from pathlib import Path
from typing import Any, Callable

from datagen.advancement.advancementbuilder import AdvancementBuilder
from datagen.globals import ADVANCEMENTS_PATH
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.simplefile import SimpleFile


class Advancement():
    advancements = dict[Identifier, "Advancement"]()
    __current_advancement = None

    @staticmethod
    def get(id: Identifier) -> "Advancement":
        return Advancement.advancements.setdefault(id, Advancement(id))
    
    @staticmethod
    def set_current(advancement: "Advancement"):
        Advancement.__current_advancement = advancement

    @staticmethod
    def get_current() -> "Advancement":
        return Advancement.__current_advancement # type: ignore

    def __init__(self, id: Identifier):
        from datagen.datapack.namespace import Namespace
        self._ns = Namespace.get(id)
        self.id = id
        self.data = dict[str, Any]()
        Advancement.advancements[id] = self

    def __invert__(self):
        self._ns.add_advancement(self)

    @staticmethod    
    def __get_data_dict(data: Any) -> Any:
        out = 0
        if isinstance(data, dict):
            out = dict[str, Any]()
            for k, v in data.items():
                if v == "None" or v == None: continue
                out[k] = Advancement.__get_data_dict(v)
        elif isinstance(data, list):
            out = list()
            for v in data:
                if v == "None" or v == None: continue
                out.append(Advancement.__get_data_dict(v))
        elif isinstance(data, Identifier):
            out = str(data)
        elif isinstance(data, set):
            out = [Advancement.__get_data_dict(v) for v in data]
        else:
            out = data
        return out

    def to_string(self) -> str:
        return json.dumps(self.__get_data_dict(self.data), indent=4)

    def to_file(self) -> "SimpleFile":
        return SimpleFile(
            Path(ADVANCEMENTS_PATH) / (self.id._path.replace(".", "/") + ".json"),
            self.to_string()
        )
    
    def do(self, func: Callable[["AdvancementBuilder"], None]) -> "Advancement":
        func(AdvancementBuilder(self))
        return self
    
    def open(self) -> "AdvancementBuilder":
        return AdvancementBuilder(self)

    def __enter__(self):
        Advancement.set_current(self)
        return AdvancementBuilder(self)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        Advancement.set_current(None) # type: ignore