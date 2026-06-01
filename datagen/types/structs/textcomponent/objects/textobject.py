
from typing import TYPE_CHECKING, Required

from datagen.types.structs.textcomponent.style import Style

class TextObject(Style):
    text: Required[str]