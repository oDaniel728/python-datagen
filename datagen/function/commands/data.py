from typing import Any, Callable, Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.data.datastorage import DataStorage
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.snbtserializer import SNBTSerializer

class Data():

    _TDataProvider = Literal["block", "entity", "storage"]

    @overload
    @staticmethod
    def get(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        scale: int | None = None,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def get(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        scale: int | None = None,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def get(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        scale: int | None = None,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def get(
        type: str,
        target: Any,
        path: str,
        scale: int | None = None,
        /
    ) -> CustomCommand:
        if ( isinstance(target, Identifier) and type == "storage" ):
            target = DataStorage(target)

        if scale is not None:
            return CustomCommand(f"data get {type} {target} {path} {scale}")
        else:
            return CustomCommand(f"data get {type} {target} {path}")

    @overload
    @staticmethod
    def merge(
        type: Literal["block"],
        target: BlockPosition,
        data: dict,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def merge(
        type: Literal["entity"],
        target: TargetSelector,
        data: dict,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def merge(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        data: dict,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def merge(
        type: str,
        target: Any,
        data: dict
    ) -> CustomCommand:
        if ( isinstance(target, Identifier) and type == "storage" ):
            target = DataStorage(target)

        _data = SNBTSerializer.serialize(data)

        return CustomCommand(f"data merge {type} {target} {_data}")