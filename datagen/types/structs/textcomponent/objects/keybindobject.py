
from typing import TYPE_CHECKING, Required

from datagen.types.structs.textcomponent.style import Style

class KeybindObject(Style):
    keybind: Required[str]