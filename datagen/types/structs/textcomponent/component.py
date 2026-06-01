from datagen.types.structs.textcomponent.objects.blocknbtobject import BlockNBTObject
from datagen.types.structs.textcomponent.objects.entitynbtobject import EntityNBTObject
from datagen.types.structs.textcomponent.objects.keybindobject import KeybindObject
from datagen.types.structs.textcomponent.objects.scoreobject import ScoreObject
from datagen.types.structs.textcomponent.objects.selectorobject import SelectorObject
from datagen.types.structs.textcomponent.objects.storagenbtobject import StorageNBTObject
from datagen.types.structs.textcomponent.objects.textobject import TextObject
from datagen.types.structs.textcomponent.objects.translatableobject import TranslateObject


Component = (
    TextObject
    | TranslateObject
    | ScoreObject
    | SelectorObject
    | KeybindObject
    | BlockNBTObject
    | EntityNBTObject
    | StorageNBTObject
)