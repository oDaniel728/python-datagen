import json
from pathlib import Path
from typing import final

from typing_extensions import Self

from datagen.datapack.namespace import Namespace
from datagen.globals import DatagenConfig
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.logger import Logger
from datagen.utils.obfuscator import Obfuscator

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
    __datapacks = set["DataPack"]()
    __current_datapack: "DataPack | None" = None

    def __del__(self):
        self.__datapacks.remove(self)

    @staticmethod
    def get_datapacks() -> set["DataPack"]:
        """Returns a set of all datapacks that have been created."""
        return DataPack.__datapacks

    @staticmethod
    def get_datapack_by_name(name: str) -> "DataPack":
        """Returns the datapack with the given name, or raises a ValueError if no such datapack exists."""
        for dp in DataPack.__datapacks:
            if dp.name == name:
                return dp
        raise ValueError(f"Datapack with name '{name}' not found")

    @staticmethod
    def get_namespace_by_identifier(id: Identifier) -> Namespace:
        """Returns the namespace with the given identifier, or raises a ValueError if no such namespace exists."""
        for dp in DataPack.__datapacks:
            for ns in dp.namespaces:
                if ns.name == id._namespace:
                    return ns
        return None # type: ignore

    @staticmethod
    def get_current_datapack() -> "DataPack":
        """Returns the currently active datapack being built, or raises a ValueError if no datapack is currently being built."""
        if DataPack.__current_datapack is None:
            raise ValueError("No datapack is currently being built")
        return DataPack.__current_datapack

    def __init__(self, name: str, description: str) -> None:
        """Initializes a new datapack with the given name and description, and adds it to the global set of datapacks."""
        self.__datapacks.add(self)
        self.name = name
        self.description = description
        self.namespaces = set[Namespace]()
        self.namespaces.add(Namespace.temp())
        self.__current_datapack = self

    def add_namespace(self, namespace: Namespace) -> Self:
        """Adds a namespace to the datapack and returns the datapack for chaining."""
        self.namespaces.add(namespace)
        return self

    def __clear(self, output: str | Path, _log_this: bool = True):
        if _log_this:
            Logger.start_task(f"Clearing output directory '{output}'")
        out = Path(output)
        if out.exists():
            for item in out.iterdir():
                if item.is_dir():
                    self.__clear(item, _log_this=False)
                else:
                    item.unlink()
            out.rmdir()
        if _log_this:
            Logger.end_task(f"Clearing output directory '{output}'")

    def build(self, output: str | Path | None = None):
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
        if not output:
            output = DatagenConfig.config["builderSettings"]["output"]
        Obfuscator.reset()
        Logger.start_task(f"Building datapack '{self.name}'")
        out = Path(output) / self.name
        self.__clear(out)
        out.mkdir(parents=True, exist_ok=True)

        def write_file(path: str | Path, content: str):
            fp = out / Path(path)
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)

        for namespace in self.namespaces:
            namespace.build(out / "data" / namespace.name)

        write_file("pack.mcmeta", json.dumps({
            "pack": {
                "pack_format": 48,
                "description": self.description
            }
        }, indent=4))
        Logger.end_task(f"Building datapack '{self.name}'")

    def __enter__(self) -> Self:
        """Enters the context of the datapack, setting it as the currently active datapack being built. Returns self for use in `with` statements."""
        self.__current_datapack = self
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        """Exits the context of the datapack, clearing the currently active datapack being built."""
        self.__current_datapack = None

    def __iadd__(self, other: Namespace | tuple[Namespace, ...]) -> Self:
        """Adds a namespace to the datapack using the `+=` operator."""
        if isinstance(other, Namespace):
            self.add_namespace(other)
        else:
            for i in other:
                self += i
        return self

    def __invert__(self):
        DataPack.__current_datapack = self
        return self