from typing import Required

from datagen.types.structs.textcomponent.objects.nbtobject import NBTObject

class BlockNBTObject(NBTObject):
    block: Required[str] # type: ignore