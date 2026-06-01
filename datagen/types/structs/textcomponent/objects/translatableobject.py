from typing import TYPE_CHECKING, NotRequired, Required

from datagen.types.structs.textcomponent.style import Style
if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.textcomponent import TextComponent

class TranslateObject(Style):
    translate: Required[str]
    with_: NotRequired["TextComponent"]