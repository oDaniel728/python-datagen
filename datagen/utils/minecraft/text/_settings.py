from typing import TYPE_CHECKING, Literal

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text._base import BaseText, BaseTextSettings
from datagen.utils.repr.keybind import KeyBind

if TYPE_CHECKING:
    from datagen.utils.scoreboard.player import ScoreboardPlayer


class LiteralTextSettings(BaseTextSettings):
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
        text: str = "",
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "text"
        self.text: str = text

    def to_dict(self) -> dict:
        return super().to_dict() | {"text": self.text}


class TranslateTextSettings(BaseTextSettings):
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
        translate: Identifier | None = None,
        fallback: str | None = None,
        with_: list[BaseText] | None = None,
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "translatable"
        self.translate: Identifier | None = translate
        self.fallback: str | None = fallback
        self.with_: list[BaseText] | None = with_

    def to_dict(self) -> dict:
        return super().to_dict() | {
            "translate": self.translate,
            "with": [t.to_string() for t in self.with_] if self.with_ else None,
        }


class ScoreTextSettings(BaseTextSettings):
    def __init__(
        self,
        *,
        player: 'ScoreboardPlayer',
        italic: bool = False,
        bold: bool = False,
        underlined: bool = False,
        strikethrough: bool = False,
        obfuscated: bool = False,
        color: 'BaseTextSettings.TextColor' = "white",
        font: Identifier | None = None,
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "score"
        self.player: 'ScoreboardPlayer' = player

    def to_dict(self) -> dict:
        return (
            super().to_dict() | {"score": {"name": str(self.player), "objective": str(self.player.objective)}}
            if self.player else {}
        )


class SelectorTextSettings(BaseTextSettings):
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
        selector: TargetSelector | None = None,
        separator: BaseText | None = None,
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "selector"
        self.selector: TargetSelector | None = selector
        self.separator: BaseText | None = separator

    def to_dict(self) -> dict:
        return super().to_dict() | {
            "selector": self.selector,
            "separator": self.separator.to_string() if self.separator else None,
        }


class KeybindTextSettings(BaseTextSettings):
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
        keybind: KeyBind | None = None,
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "keybind"
        self.keybind: KeyBind | None = keybind

    def to_dict(self) -> dict:
        return super().to_dict() | {"keybind": self.keybind}


class NBTTextSettings(BaseTextSettings):
    TSource = Literal["block", "entity", "storage"]

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
        source: 'NBTTextSettings.TSource' = "block",
        nbt: str = "",
        interpret: bool = False,
        block: str | None = None,
        entity: str | None = None,
        storage: str | None = None,
        separator: BaseText | None = None,
    ) -> None:
        super().__init__(
            italic=italic,
            bold=bold,
            underlined=underlined,
            strikethrough=strikethrough,
            obfuscated=obfuscated,
            color=color,
            font=font,
        )
        self.type = "nbt"
        self.source: NBTTextSettings.TSource = source
        self.nbt: str = nbt
        self.interpret: bool = interpret
        self.block: str | None = block
        self.entity: str | None = entity
        self.storage: str | None = storage
        self.separator: BaseText | None = separator

    def to_dict(self) -> dict:
        return super().to_dict() | {
            "nbt": self.nbt,
            "block": self.block,
            "entity": self.entity,
            "storage": self.storage,
            "separator": self.separator.to_string() if self.separator else None,
        }
