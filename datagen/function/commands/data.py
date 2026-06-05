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

    _TModifyType = Literal["append", "insert", "merge", "prepend", "set"]
    _TModifyMethods = Literal["from", "string", "value"]

    @overload
    @staticmethod
    def modify(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        modify_type: Literal["merge"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        string: Literal[True],
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
        start: int,
        end: int,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        modify_type: Literal["merge"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        string: Literal[True],
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
        start: int,
        end: int,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        modify_type: Literal["merge"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        value: Any,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def modify(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        modify_type: Literal["append", "insert", "prepend", "set"],
        *,
        string: Literal[True],
        from_provider: _TDataProvider,
        from_target: Any,
        from_path: str,
        start: int,
        end: int,
    ) -> CustomCommand: ...

    @staticmethod
    def modify(
        type: str,
        target: Any,
        path: str,
        modify_type: str,
        *,
        value: Any | None = None,
        from_provider: str | None = None,
        from_target: Any | None = None,
        from_path: str | None = None,
        string: bool = False,
        start: int | None = None,
        end: int | None = None,
    ) -> CustomCommand:
        if isinstance(target, Identifier) and type == "storage":
            target = DataStorage(target)

        if modify_type == "merge":
            if value is None:
                raise ValueError("merge requires a value")

            _value = SNBTSerializer._serialize_value(value)
            return CustomCommand(f"data modify {type} {target} {path} merge {_value}")

        if value is not None:
            _value = SNBTSerializer._serialize_value(value)
            return CustomCommand(
                f"data modify {type} {target} {path} {modify_type} value {_value}"
            )

        if from_provider is None or from_target is None or from_path is None:
            raise ValueError(
                "from_provider, from_target and from_path are required when no value is provided"
            )

        if string:
            if start is None or end is None:
                raise ValueError("string modify requires start and end indexes")

            return CustomCommand(
                f"data modify {type} {target} {path} {modify_type} string "
                f"{from_provider} {from_target} {from_path} {start} {end}"
            )

        return CustomCommand(
            f"data modify {type} {target} {path} {modify_type} from "
            f"{from_provider} {from_target} {from_path}"
        )
    
    @overload
    @staticmethod
    def remove(
        type: Literal["block"],
        target: BlockPosition,
        path: str,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def remove(
        type: Literal["entity"],
        target: TargetSelector,
        path: str,
        /
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def remove(
        type: Literal["storage"],
        target: DataStorage | Identifier,
        path: str,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def remove(
        type: str,
        target: Any,
        path: str
    ) -> CustomCommand:
        if isinstance(target, Identifier) and type == "storage":
            target = DataStorage(target)

        return CustomCommand(f"data remove {type} {target} {path}")
