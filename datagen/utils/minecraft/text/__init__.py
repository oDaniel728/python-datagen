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
    KeybindText,
    LiteralText,
    NBTText,
    ScoreText,
    SelectorText,
    TranslatableText,
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
    literal = LiteralText
    translate = TranslatableText
    score = ScoreText
    selector = SelectorText
    keybind = KeybindText
    nbt = NBTText

    @overload
    @staticmethod
    def of(settings: LiteralTextSettings) -> LiteralText: ...

    @overload
    @staticmethod
    def of(settings: TranslateTextSettings) -> TranslatableText: ...

    @overload
    @staticmethod
    def of(settings: ScoreTextSettings) -> ScoreText: ...

    @overload
    @staticmethod
    def of(settings: SelectorTextSettings) -> SelectorText: ...

    @overload
    @staticmethod
    def of(settings: KeybindTextSettings) -> KeybindText: ...

    @overload
    @staticmethod
    def of(settings: NBTTextSettings) -> NBTText: ...

    @staticmethod
    def of(settings: BaseTextSettings):
        if isinstance(settings, LiteralTextSettings):
            return LiteralText(settings.text, settings)
        elif isinstance(settings, TranslateTextSettings):
            return TranslatableText(_unNull @ settings.translate, settings)
        elif isinstance(settings, ScoreTextSettings):
            return ScoreText(settings.player, settings)
        elif isinstance(settings, SelectorTextSettings):
            return SelectorText(_unNull @ settings.selector, settings)
        elif isinstance(settings, KeybindTextSettings):
            return KeybindText(_unNull @ settings.keybind, settings)
        elif isinstance(settings, NBTTextSettings):
            return NBTText(settings.nbt, settings.source, settings)
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
    "LiteralText",
    "TranslatableText",
    "ScoreText",
    "SelectorText",
    "KeybindText",
    "NBTText",
]
