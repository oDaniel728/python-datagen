#type: ignore
from typing import Self
from uuid import uuid4

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.types.util.counter import Counter
from datagen.utils.minecraft.identifier import Identifier

_C = Counter()
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

    def __init__(self, datapack: DataPack | None = None):
        super().__init__(Namespace.temp().identifier(f"fun{_C}"))
        self.datapack = datapack or DataPack.get_current_datapack()
        self.datapack.add_namespace(Namespace.temp())
        Namespace.temp().add(self)