from __future__ import annotations

from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.utils.minecraft.blockposition import BlockPosition
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.item import Item
from datagen.utils.repr.itemstack import ItemStack
from datagen.utils.repr.slot_range import SlotRange


ItemLike = Item | ItemStack | str


class ReplaceItem():

    @overload
    @staticmethod
    def replace(
        type: Literal["block"],
        target: BlockPosition,
        slot: SlotRange,
        with_item: ItemLike,
        /
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def replace(
        type: Literal["entity"],
        target: TargetSelector,
        slot: SlotRange,
        with_item: ItemLike,
        /
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def replace(
        type: Literal["block"],
        target: BlockPosition,
        slot: SlotRange,
        from_block: BlockPosition,
        from_slot: SlotRange,
        /
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def replace(
        type: Literal["block"],
        target: BlockPosition,
        slot: SlotRange,
        from_entity: TargetSelector,
        from_slot: SlotRange,
        /
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def replace(
        type: Literal["entity"],
        target: TargetSelector,
        slot: SlotRange,
        from_block: BlockPosition,
        from_slot: SlotRange,
        /
    ) -> CustomCommand: ...

    @overload
    @staticmethod
    def replace(
        type: Literal["entity"],
        target: TargetSelector,
        slot: SlotRange,
        from_entity: TargetSelector,
        from_slot: SlotRange,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def replace(
        type: str,
        target: object,
        slot: SlotRange,
        arg1: object,
        arg2: object | None = None,
        /
    ) -> CustomCommand:
        if isinstance(arg1, (Item, ItemStack, str)):
            if arg2 is not None:
                raise ValueError(
                    "with_item replacement accepts only four positional arguments"
                )
            return CustomCommand(f"item replace {type} {target} {slot} with {arg1}")

        if not isinstance(arg2, SlotRange):
            raise ValueError(
                "from replacement requires a target slot as the fifth positional argument"
            )

        if isinstance(arg1, BlockPosition):
            return CustomCommand(
                f"item replace {type} {target} {slot} from block {arg1} {arg2}"
            )

        if isinstance(arg1, TargetSelector):
            return CustomCommand(
                f"item replace {type} {target} {slot} from entity {arg1} {arg2}"
            )

        raise ValueError(
            "replace requires either an item to place or a block/entity source plus a slot"
        )
