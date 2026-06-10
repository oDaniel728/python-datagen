from typing import overload
from warnings import deprecated

from datagen.utils.minecraft.text._base import BaseText, BaseTextSettings
from datagen.utils.minecraft.text._settings import (
    KeybindTextSettings,
    LiteralTextSettings,
    NBTTextSettings,
    ScoreTextSettings,
    SelectorTextSettings,
    TranslateTextSettings,
)
from datagen.utils.minecraft.text._components import (
    keybind,
    literal,
    nbt,
    score,
    selector,
    translate,
)


class __notNone__():
    @staticmethod
    def __matmul__[T](other: T | None) -> T:
        if other is None:
            raise ValueError("Value cannot be None")
        return other


_unNull = __notNone__()


class Text:
    @deprecated("Do not use __init__ in Text, use .literal or .translate instead")
    def __init__(self):
        pass

    BaseTextSettings = BaseTextSettings
    LiteralTextSettings = LiteralTextSettings
    TranslateTextSettings = TranslateTextSettings
    ScoreTextSettings = ScoreTextSettings
    SelectorTextSettings = SelectorTextSettings
    KeybindTextSettings = KeybindTextSettings
    NBTTextSettings = NBTTextSettings

    BaseText = BaseText
    literal = literal
    translate = translate
    score = score
    selector = selector
    keybind = keybind
    nbt = nbt

    @overload
    @staticmethod
    def of(settings: LiteralTextSettings) -> literal: ...

    @overload
    @staticmethod
    def of(settings: TranslateTextSettings) -> translate: ...

    @overload
    @staticmethod
    def of(settings: ScoreTextSettings) -> score: ...

    @overload
    @staticmethod
    def of(settings: SelectorTextSettings) -> selector: ...

    @overload
    @staticmethod
    def of(settings: KeybindTextSettings) -> keybind: ...

    @overload
    @staticmethod
    def of(settings: NBTTextSettings) -> nbt: ...

    @staticmethod
    def of(settings: BaseTextSettings):
        if isinstance(settings, LiteralTextSettings):
            return literal(settings.text, settings)
        elif isinstance(settings, TranslateTextSettings):
            return translate(_unNull @ settings.translate, settings)
        elif isinstance(settings, ScoreTextSettings):
            return score(settings.player, settings)
        elif isinstance(settings, SelectorTextSettings):
            return selector(_unNull @ settings.selector, settings)
        elif isinstance(settings, KeybindTextSettings):
            return keybind(_unNull @ settings.keybind, settings)
        elif isinstance(settings, NBTTextSettings):
            return nbt(settings.nbt, settings.source, settings)
        raise ValueError(f"Invalid settings type: {type(settings)}")


__all__ = [
    "Text",
    "BaseTextSettings",
    "BaseText",
    "LiteralTextSettings",
    "TranslateTextSettings",
    "ScoreTextSettings",
    "SelectorTextSettings",
    "KeybindTextSettings",
    "NBTTextSettings",
    "literal",
    "translate",
    "score",
    "selector",
    "keybind",
    "nbt",
]
