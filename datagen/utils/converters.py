from typing import Any, Protocol

from datagen.types.util.holder import Holder
from datagen.utils.minecraft.identifier import Identifier


class Dictionary[K, V]():
    class HasToDict(Protocol):
        def to_dict(self) -> dict[K, V]: ...
    type TDictionaryProvider = HasToDict | dict | Any
    @staticmethod
    def auto(v: Any) -> dict[K, V]:
        if isinstance(v, dict):
            return v
        elif hasattr(v, "to_dict") and callable(getattr(v, "to_dict")):
            return v.to_dict()
        elif hasattr(v, "dict"):
            if callable(getattr(v, "dict")):
                return v.dict()
            else:
                return v.dict
        else:
            raise ValueError(f"Cannot convert {v}:{type(v)} to Dictionary")
        
class IdentifierConverter():
    @staticmethod
    def auto(v: Any) -> Identifier:
        if isinstance(v, dict):
            if "id" in v:
                return IdentifierConverter.auto(v["id"])
            else:
                raise ValueError("Cannot convert dict to Identifier, missing 'id' key")
        elif isinstance(v, str):
            return Identifier.of(v)
        elif isinstance(v, Identifier):
            return v
        elif isinstance(v, (tuple, list)) and len(v) == 2:
            return Identifier.of(v[0], v[1])
        elif isinstance(v, Holder):
            return IdentifierConverter.auto(v.get())
        else:
            raise ValueError(f"Cannot convert {v}:{type(v)} to Identifier")