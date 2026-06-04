from datagen.function.commands.data.datastorage import DataStorage
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier


class Data():
    @staticmethod
    def storage(id: Identifier) -> "DataStorage":
        return DataStorage(id)