import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from datagen.utils.minecraft.text._base import BaseText


class DatagenEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        from datagen.utils.minecraft.text._base import BaseText
        if isinstance(obj, BaseText):
            return str(obj)
        if hasattr(obj, "to_dict") and callable(getattr(obj, "to_dict")):
            return obj.to_dict()
        if hasattr(obj, "to_string") and callable(getattr(obj, "to_string")):
            return str(obj)
        return super().default(obj)


def dumps(obj: Any, **kwargs: Any) -> str:
    if "cls" not in kwargs:
        kwargs["cls"] = DatagenEncoder
    return json.dumps(obj, **kwargs)
