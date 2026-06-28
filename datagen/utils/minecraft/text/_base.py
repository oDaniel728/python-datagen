import json
from typing import Literal

from datagen.types.protocols.todict import ToDict
from datagen.types.protocols.tostring import ToString
from datagen.utils.json_encoder import dumps
from datagen.utils.minecraft.identifier import Identifier


def _remove_nulls[T](d: T) -> T:
    if isinstance(d, dict):
        return {k: _remove_nulls(v) for k, v in d.items() if v is not None} # type: ignore
    elif isinstance(d, list):
        return [_remove_nulls(v) for v in d if v is not None] # type: ignore
    else:
        return d

class BaseTextSettings(ToDict):
    TextColor = Literal[
        "black",
        "dark_blue",
        "dark_green",
        "dark_aqua",
        "dark_red",
        "dark_purple",
        "gold",
        "gray",
        "dark_gray",
        "blue",
        "green",
        "aqua",
        "red",
        "light_purple",
        "yellow",
        "white",
    ] | str
    TextType = Literal[
        "text",
        "translatable",
        "score",
        "selector",
        "keybind",
        "nbt",
    ]

    def __init__(
        self,
        *,
        italic: bool = False,
        bold: bool = False,
        underlined: bool = False,
        strikethrough: bool = False,
        obfuscated: bool = False,
        color: 'BaseTextSettings.TextColor' = "white",
        font: Identifier | None = None,
    ) -> None:
        self.type: BaseTextSettings.TextType = "text"
        self.italic: bool = italic
        self.bold: bool = bold
        self.underlined: bool = underlined
        self.strikethrough: bool = strikethrough
        self.obfuscated: bool = obfuscated
        self.color: BaseTextSettings.TextColor = color
        self.font: Identifier | None = font

    def to_dict(self) -> dict:
        return _remove_nulls({
            "type": self.type,
            "italic": self.italic,
            "bold": self.bold,
            "underlined": self.underlined,
            "strikethrough": self.strikethrough,
            "obfuscated": self.obfuscated,
            "color": self.color,
            "font": self.font.to_string() if self.font else None,
        })

    def to_string(self) -> str:
        return dumps(self.to_dict())

class BaseText(ToString, ToDict):
    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        return dumps(_remove_nulls(self.to_dict()))
    
    @staticmethod
    def components(*components: 'BaseText') -> 'list[BaseText]':
        return list(components)
