
from typing import Required

from datagen.types.structs.textcomponent.objects.nbtobject import NBTObject


class StorageNBTObject(NBTObject):
    storage: Required[str] # type: ignore