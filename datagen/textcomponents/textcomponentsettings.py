
from dataclasses import dataclass

from datagen.types.literals.textcolor import TextColor


@dataclass
class TextComponentSettings():
    color: "TextColor | str"
    bold: bool
    italic: bool
    underlined: bool
    strikethrough: bool
    obfuscated: bool

    @staticmethod
    def default():
        return TextComponentSettings(
            color="white",
            bold=False,
            italic=False,
            underlined=False,
            strikethrough=False,
            obfuscated=False
        )
    
    def to_dict(self) -> dict:
        return {
            "color": self.color,
            "bold": self.bold,
            "italic": self.italic,
            "underlined": self.underlined,
            "strikethrough": self.strikethrough,
            "obfuscated": self.obfuscated
        }