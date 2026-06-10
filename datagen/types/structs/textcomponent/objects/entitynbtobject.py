from typing import Required

from datagen.types.structs.textcomponent.objects.nbtobject import NBTObject


class EntityNBTObject(NBTObject):
    entity: Required[str] # type: ignore