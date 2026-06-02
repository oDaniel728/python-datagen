import json
from typing import Any, Literal, override, override
from warnings import deprecated

from typing import overload

from datagen.types.protocols.todict import ToDict
from datagen.types.protocols.tostring import ToString
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.keybind import KeyBind


class Text():
    @deprecated("Do not use __init__ in Text, use .literal or .translate instead")
    def __init__(self):
        pass

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
            "nbt"
        ]
        def __init__(self,
            *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None
        ) -> None:
            self.type: Text.BaseTextSettings.TextType = "text"
            self.italic: bool = italic
            self.bold: bool = bold
            self.underlined: bool = underlined
            self.strikethrough: bool = strikethrough
            self.obfuscated: bool = obfuscated

            self.color: Text.BaseTextSettings.TextColor = color

            self.font: Identifier | None = font
        def to_dict(self) -> dict:
            return {
                "type": self.type,
                "italic": self.italic,
                "bold": self.bold,
                "underlined": self.underlined,
                "strikethrough": self.strikethrough,
                "obfuscated": self.obfuscated,
                "color": self.color,
                "font": self.font.to_string() if self.font else None
            }
        def to_string(self) -> str:
            return json.dumps(self.to_dict())

    class LiteralTextSettings(BaseTextSettings):
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            text: str = ""
        ) -> None:
            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "text"
            self.text: str = text

        def to_dict(self) -> dict:
            return super().to_dict() | {"text": self.text}

    class TranslateTextSettings(BaseTextSettings):
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            translate: Identifier | None = None,
            fallback: str | None = None,
            with_: list[Text.BaseText] | None = None
        ) -> None:
            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "translatable"
            self.translate: Identifier | None = translate
            self.fallback: str | None = fallback
            self.with_: list[Text.BaseText] | None = with_

        def to_dict(self) -> dict:
            return super().to_dict() | {"translate": self.translate, "with": [t.to_string() for t in self.with_] if self.with_ else None}

    class ScoreTextSettings(BaseTextSettings):
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            name: str = "",
            objective: str = ""
        ) -> None:
            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "score"
            self.name: str = name
            self.objective: str = objective

        def to_dict(self) -> dict:
            return super().to_dict() | {"score": {"name": self.name, "objective": self.objective}}
        
    class SelectorTextSettings(BaseTextSettings):
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            selector: TargetSelector | None = None,
            separator: Text.BaseText | None = None
        ) -> None:

            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "selector"
            self.selector: TargetSelector | None = selector
            self.separator: Text.BaseText | None = separator

        def to_dict(self) -> dict:
            return super().to_dict() | {"selector": self.selector, "separator": self.separator.to_string() if self.separator else None}

    class KeybindTextSettings(BaseTextSettings):
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            keybind: KeyBind | None = None
        ) -> None:
            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "keybind"
            self.keybind: KeyBind | None = keybind

        def to_dict(self) -> dict:
            return super().to_dict() | {"keybind": self.keybind}

    class NBTTextSettings(BaseTextSettings):
        TSource = Literal["block", "entity", "storage"]
        def __init__(self, *,
            italic: bool = False,
            bold: bool = False,
            underlined: bool = False,
            strikethrough: bool = False,
            obfuscated: bool = False,
            color: 'Text.BaseTextSettings.TextColor' = "white",
            font: Identifier | None = None,
            source: Text.NBTTextSettings.TSource = "block",
            nbt: str = "",
            interpret: bool = False,
            block: str | None = None,
            entity: str | None = None,
            storage: str | None = None,
            separator: Text.BaseText | None = None
        ) -> None:
            super().__init__(
                italic=italic,
                bold=bold,
                underlined=underlined,
                strikethrough=strikethrough,
                obfuscated=obfuscated,
                color=color,
                font=font
            )
            self.type = "nbt"
            self.source: Text.NBTTextSettings.TSource = source
            self.nbt: str = nbt
            self.interpret: bool = interpret
            self.block: str | None = block
            self.entity: str | None = entity
            self.storage: str | None = storage
            self.separator: Text.BaseText | None = separator

        def to_dict(self) -> dict:
            return super().to_dict() | {"nbt": self.nbt, "block": self.block, "entity": self.entity, "storage": self.storage, "separator": self.separator.to_string() if self.separator else None}

    class BaseText(ToString, ToDict): 
        def to_string(self) -> str:
            return json.dumps({k: v for k, v in self.to_dict().items() if v is not None})

    class literal(BaseText):
        def __init__(self, value: str, settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.value = value
            self.settings = settings

        def to_dict(self) -> dict:
            return self.settings.to_dict() | {"type": "text"} | {"text": self.value} if self.settings else {"text": self.value}

    
    class translate(BaseText):
        def __init__(self, value: Identifier, settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.value = value
            self.settings = settings

        def to_dict(self) -> dict:
            return self.settings.to_dict() | {"type": "translatable"} | {"translate": self.value.to_string()} if self.settings else {"translate": self.value.to_string()}

    class score(BaseText):
        def __init__(self, name: str, objective: str, settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.name = name
            self.objective = objective
            self.settings = settings

        def to_dict(self) -> dict:
            return self.settings.to_dict() | {"type": "score"} | {"score": {"name": self.name, "objective": self.objective}} if self.settings else {"score": {"name": self.name, "objective": self.objective}}
        
    class selector(BaseText):
        def __init__(self, selector: TargetSelector, settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.selector = selector
            self.settings = settings

        def to_string(self) -> str:
            return json.dumps(self.settings.to_dict() | {"type": "selector"} | {"selector": self.selector.to_string()} if self.settings else {"selector": self.selector.to_string()})
        
    class keybind(BaseText):
        def __init__(self, keybind: KeyBind, settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.keybind = keybind
            self.settings = settings

        def to_dict(self) -> dict:
            return self.settings.to_dict() | {"type": "keybind"} | {"keybind": self.keybind} if self.settings else {"keybind": self.keybind}

    class nbt(BaseText):
        def __init__(self, nbt: str, source: Text.NBTTextSettings.TSource = "block", settings: 'Text.BaseTextSettings | None' = None) -> None:
            self.nbt = nbt
            self.source = source
            self.settings = settings

        def to_dict(self) -> dict:
            return self.settings.to_dict() | {"type": "nbt"} | {"nbt": self.nbt, self.source: self.nbt} if self.settings else {"nbt": self.nbt, self.source: self.nbt}

    @overload
    @staticmethod
    def of(settings: 'Text.LiteralTextSettings') -> 'Text.literal': ...

    @overload
    @staticmethod
    def of(settings: 'Text.TranslateTextSettings') -> 'Text.translate': ...

    @overload
    @staticmethod
    def of(settings: 'Text.ScoreTextSettings') -> 'Text.score': ...

    @overload
    @staticmethod
    def of(settings: 'Text.SelectorTextSettings') -> 'Text.selector': ...

    @overload
    @staticmethod
    def of(settings: 'Text.KeybindTextSettings') -> 'Text.keybind': ...

    @overload
    @staticmethod
    def of(settings: 'Text.NBTTextSettings') -> 'Text.nbt': ...

    @staticmethod
    def of(settings: BaseTextSettings):
        typeMap = {
            Text.LiteralTextSettings: Text.literal,
            Text.TranslateTextSettings: Text.translate,
            Text.ScoreTextSettings: Text.score,
            Text.SelectorTextSettings: Text.selector,
            Text.KeybindTextSettings: Text.keybind,
            Text.NBTTextSettings: Text.nbt
        }
        for settingsType, textType in typeMap.items():
            if isinstance(settings, settingsType):
                return textType("", settings)
        raise ValueError(f"Invalid settings type: {type(settings)}")