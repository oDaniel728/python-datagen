from datagen.datapack.namespace import Namespace
from datagen.function.commands.data.datastorage import DataStorage
from datagen.utils.minecraft.identifier import Identifier


class DataFunctionArgument(DataStorage):

    def __init__(self, values: list[DataStorage.TAny]):
        super().__init__(Namespace.temp/"data_function_argument", {})
        self.values = {"args": values}