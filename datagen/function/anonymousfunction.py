#type: ignore
from typing import Self
from uuid import uuid4

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class AnonymousFunction(Function):
    """
    # Anonymous Function
    - Inherits from `Function`
    ## Summary
    Represents an anonymous function that is automatically generated and managed by the library. Anonymous functions are created with a unique identifier based on the number of existing functions in a temporary namespace, and are added to that namespace and the current datapack. They can be used for temporary or one-off functions that do not need to be referenced by name, and are automatically cleaned up when they are no longer needed.
    ## Examples
    - Creating an anonymous function and running it immediately
    ```python
    with AnonymousFunction(DataPack.get_current_datapack()) as f:
        ~ Say("This is an anonymous function!")
    ```
    """

    def __new__(cls, datapack: DataPack) -> Self:
        id = Namespace.temp.identifier(f"fun{len(Namespace.temp.functions)}")
        if id in cls._Function__funcs:
            return cls._Function__funcs[id]
        else:
            func = super(AnonymousFunction, cls).__new__(cls, id)
            cls._Function__funcs[id] = func
            return func

    def __init__(self, datapack: DataPack):
        super().__init__(Namespace.temp.identifier(f"fun{len(Namespace.temp.functions)}"))
        self.datapack = datapack
        self.datapack.add_namespace(Namespace.temp)
        Namespace.temp.add(self)