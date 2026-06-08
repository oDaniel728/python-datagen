from pathlib import Path
from typing import final

from typing_extensions import Self

from datagen.datapack.namespace import Namespace
from datagen.utils.minecraft.identifier import Identifier

@final
class DataPack:
    """
    # Data Pack
    - See https://minecraft.wiki/w/Data_pack
    ## Summary
    Represents a Minecraft datapack, which is a collection of namespaces 
    and resources that can be loaded into the game. Each datapack has a 
    name, description, and a set of namespaces. The datapack can be built 
    into a folder structure that Minecraft recognizes, and can be used in 
    the game to add new features, items, or mechanics.

    The DataPack class also manages a global set of all datapacks and the 
    currently active datapack being built. This allows for easy retrieval of 
    datapacks and namespaces by name or identifier, and ensures that only one 
    datapack is being built at a time.

    ## Examples
    - Hello World Datapack
    ```python
        from datagen.datapack.datapack import DataPack
        from datagen.datapack.namespace import Namespace
        from datagen.function.commands.say import Say
        from datagen.function.function import Function

        def main():
            with DataPack("pack", "a pack") as dp:
                with Namespace("pack") as ns:
                    with Function(ns / "hello") as f:
                        ~ Say("Hello, world!")
                dp.add_namespace(ns)
            dp.build()
    ```

    - Hello World Datapack without with statements
    ```python
        from datagen.datapack.datapack import DataPack
        from datagen.datapack.namespace import Namespace
        from datagen.function.commands.say import Say
        from datagen.function.function import Function

        def main():
            dp = DataPack("pack", "a pack")
            ns = Namespace("pack")
            f = Function(ns / "hello")
            f.add_command(Say("Hello, world!"))
            dp.add_namespace(ns)
            dp.build()
    ```
    """

    name: str
    """The name of the datapack. This is used in the `pack.mcmeta` file and should be unique among all datapacks."""
    description: str
    """A brief description of the datapack. This is used in the `pack.mcmeta` file."""
    namespaces: set[Namespace]
    """A set of namespaces contained within the datapack."""

    def __init__(self, name: str, description: str) -> None:
        """Initializes a new datapack with the given name and description, and adds it to the global set of datapacks."""
        ...

    def __del__(self) -> None: ...

    @staticmethod
    def get_datapacks() -> set[DataPack]:
        """Returns a set of all datapacks that have been created."""
        ...

    @staticmethod
    def get_datapack_by_name(name: str) -> DataPack:
        """Returns the datapack with the given name, or raises a ValueError if no such datapack exists."""
        ...

    @staticmethod
    def get_namespace_by_identifier(id: Identifier) -> Namespace:
        """Returns the namespace with the given identifier, or raises a ValueError if no such namespace exists."""
        ...

    @staticmethod
    def get_current_datapack() -> DataPack:
        """Returns the currently active datapack being built, or raises a ValueError if no datapack is currently being built."""
        ...

    def add_namespace(self, namespace: Namespace) -> Self:
        """Adds a namespace to the datapack and returns the datapack for chaining."""
        ...

    def build(self, output: str | Path | None = None) -> None:
        """
        Builds the datapack into the output directory.

        Creates the necessary folder structure and writes the `pack.mcmeta` file,
        as well as building each namespace and its resources into the appropriate
        subdirectories. The output directory is cleared before building to ensure
        that there are no leftover files from previous builds.

        Args:
            output: Path to the output directory. Defaults to the value set in
                    `DatagenConfig.config["builderSettings"]["output"]`.
        """
        ...

    def __enter__(self) -> Self:
        """
        Enters the context of the datapack, setting it as the currently active
        datapack being built. Returns self for use in `with` statements.
        """
        ...

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """
        Exits the context of the datapack, clearing the currently active
        datapack being built.
        """
        ...

    def __iadd__(self, other: Namespace) -> Self: 
        """Adds a namespace to the datapack using the `+=` operator."""
        ...