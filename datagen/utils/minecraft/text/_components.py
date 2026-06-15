from typing import TYPE_CHECKING

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._base import BaseText, BaseTextSettings
from datagen.utils.minecraft.text._settings import NBTTextSettings
from datagen.utils.repr.keybind import KeyBind

if TYPE_CHECKING:
    from datagen.utils.scoreboard.player import ScoreboardPlayer


class LiteralText(BaseText):
    EMPTY: "LiteralText"
    def __init__(self, value: str, settings: BaseTextSettings | None = None) -> None:
        self.value = value
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "text"} | {"text": self.value}
            if self.settings
            else {"text": self.value}
        )
LiteralText.EMPTY = LiteralText("")

class TranslatableText(BaseText):
    def __init__(self, value: Identifier, settings: BaseTextSettings | None = None) -> None:
        self.value = value
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "translatable"} | {"translate": self.value.to_string()}
            if self.settings
            else {"translate": self.value.to_string()}
        )


class ScoreText(BaseText):
    def __init__(self, player: 'ScoreboardPlayer', settings: BaseTextSettings | None = None) -> None:
        self.player = player
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "score"} | {"score": {"name": str(self.player.name), "objective": str(self.player.objective)}}
            if self.settings
            else {"score": {"name": str(self.player), "objective": str(self.player.objective)}}
        )


class SelectorText(BaseText):
    def __init__(self, selector: TargetSelector, settings: BaseTextSettings | None = None) -> None:
        self.selector = selector
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "selector"} | {"selector": self.selector.to_string()}
            if self.settings
            else {"selector": self.selector.to_string()}
        )


class KeybindText(BaseText):
    def __init__(self, keybind: KeyBind, settings: BaseTextSettings | None = None) -> None:
        self.keybind = keybind
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "keybind"} | {"keybind": self.keybind}
            if self.settings
            else {"keybind": self.keybind}
        )


class NBTText(BaseText):
    def __init__(self, nbt: str, source: NBTTextSettings.TSource = "block", settings: BaseTextSettings | None = None) -> None:
        self.nbt = nbt
        self.source = source
        self.settings = settings

    def to_dict(self) -> dict:
        return (
            self.settings.to_dict() | {"type": "nbt"} | {"nbt": self.nbt, self.source: self.nbt}
            if self.settings
            else {"nbt": self.nbt, self.source: self.nbt}
        )
