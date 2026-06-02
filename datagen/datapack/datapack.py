import json
from pathlib import Path
from typing import final

from typing_extensions import Self

from datagen.datapack.namespace import Namespace
from datagen.function.function import Function
from datagen.globals import DatagenConfig
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.logger import Logger

@final
class DataPack():

    __datapacks = set["DataPack"]()

    def __del__(self):
        self.__datapacks.remove(self)

    @staticmethod
    def get_datapacks() -> set["DataPack"]:
        return DataPack.__datapacks
    
    @staticmethod
    def get_datapack_by_name(name: str) -> "DataPack":
        for dp in DataPack.__datapacks:
            if dp.name == name:
                return dp
        raise ValueError(f"Datapack with name '{name}' not found")
    @staticmethod
    def get_namespace_by_identifier(id: Identifier) -> Namespace:
        for dp in DataPack.__datapacks:
            for ns in dp.namespaces:
                if ns.name == id._namespace:
                    return ns
        return Namespace.get(id)
    
    def __init__(self, name: str, description: str) -> None:
        self.__datapacks.add(self)
        self.name = name
        self.description = description
        self.namespaces = set[Namespace]()

    def add_namespace(self, namespace: Namespace) -> Self:
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
        if not output:
            output = DatagenConfig.config["builderSettings"]["output"]
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
