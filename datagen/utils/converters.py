from typing import Any, Protocol


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
            raise ValueError(f"Cannot convert {v} to Dictionary")