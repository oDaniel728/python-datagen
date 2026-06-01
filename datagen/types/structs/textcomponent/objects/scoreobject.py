from typing import TYPE_CHECKING, Required

from datagen.types.structs.textcomponent.style import Style
if TYPE_CHECKING:
    from datagen.types.structs.textcomponent.other.scorevalue import ScoreValue

class ScoreObject(Style):
    score: Required[ScoreValue]