from math import ceil
from typing import overload

from datagen.entitytag import EntityTag
from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.execute import Execute
from datagen.function.commands._return import Return
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.types.util.counter import Counter
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.position3 import Position3
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagen.utils.scoreboard.player import ScoreboardPlayer
from datagen.utils.minecraft.text import Text

_counter = Counter()

class RayCaster():
    """Creates recursive raycast functions for Minecraft datapacks.

    Each method creates a ``step`` and ``hit`` helper function in the
    temp namespace, then returns a ``CommandArray`` that sets up the
    scoreboard and starts the raycast.

    The step function calls itself via ``positioned ^ ^ ^<step>``,
    advancing one step per call.  This keeps the function size constant
    (independent of the total ray length) at the cost of one function
    call per step at runtime.

    Examples:

        >>> with Function(Identifier.of("my_pack:shoot")) as f:
        ...     ~ RayCaster.on_block_hit(
        ...         block=Identifier.of("minecraft:stone"),
        ...         c=Execute().RUN(Say("Found stone!")),
        ...         step=1.0,
        ...         length=Range.max(64),
        ...     )
    """

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _fmt_step(d: float) -> str:
        if d == int(d):
            return str(int(d))
        return f"{d:g}"

    @staticmethod
    def _step_str(step: float) -> str:
        return RayCaster._fmt_step(round(step, 6))

    @staticmethod
    def _has_state(block: Block) -> bool:
        settings = block.settings  # type: ignore
        return bool(settings.get_block_state()) or bool(settings.get_block_entity_data())  # type: ignore

    @staticmethod
    def _max_steps(length: Range, step: float) -> int:
        if length.end is None:
            return 64
        return ceil(length.end / step)

    # -- block hit ---------------------------------------------------------

    @overload
    @staticmethod
    def on_block_hit(
        block: Identifier,
        hit: Command | CommandArray | None = None,
        step_f: Command | CommandArray | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray: ...

    @overload
    @staticmethod
    def on_block_hit(
        block: Block,
        hit: Command | CommandArray | None = None,
        step_f: Command | CommandArray | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray: ...

    @staticmethod
    def on_block_hit(
        block: Identifier | Block,
        hit: Command | CommandArray | None = None,
        step_f: Command | CommandArray | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray:
        uid: int = _counter.get()
        s_step: str = RayCaster._step_str(step)
        max_dist: int = RayCaster._max_steps(length, step)

        dist_obj: ScoreboardObjective = Scoreboard.objective(
            f"__ray_d_{uid}", Text.literal(""), ObjectiveCriterion.DUMMY,
        )
        max_obj: ScoreboardObjective = Scoreboard.objective(
            f"__ray_m_{uid}", Text.literal(""), ObjectiveCriterion.DUMMY,
        )
        dist: ScoreboardPlayer = dist_obj.player(TargetSelector.SELF)
        maximum: ScoreboardPlayer = max_obj.player(TargetSelector.SELF)

        block_obj: Block = Block(block) if isinstance(block, Identifier) else block
        has_state: bool = RayCaster._has_state(block_obj)
        block_str: str = str(block_obj) if has_state else str(block_obj.id)

        # hit_func: Function = Function(Identifier.of("temp", f"__raycast_{uid}_h"))
        # step_func: Function = Function(Identifier.of("temp", f"__raycast_{uid}_s"))
        hit_func: Function = Function()
        step_func: Function = Function()

        with hit_func:
            if hit is not None:
                ~ hit
            ~ Return.fail()

        with step_func:
            if step_f: ~ step_f
            ~ dist.add(1)
            ~ Execute().IF(
                lambda _c, d=dist, m=maximum: _c.score(d, ">", m)
            ).RUN(Return.fail())

            # hit branch — block matches
            if has_state:
                ~ CustomCommand(
                    f"execute positioned ^ ^ ^{s_step} "
                    f"if block ~ ~ ~ {block_str} "
                    f"run function {hit_func.id}"
                )
            else:
                ~ Execute().POSITIONED(Position3("^", "^", f"^{s_step}")).IF(
                    lambda _c, b=block_obj: _c.block(b, Position3("~", "~", "~"))  # type: ignore
                ).RUN(hit_func)

            # step branch — block NOT the target AND replaceable → recurse
            if has_state:
                ~ CustomCommand(
                    f"execute positioned ^ ^ ^{s_step} "
                    f"unless block ~ ~ ~ {block_str} "
                    f"if block ~ ~ ~ #minecraft:replaceable "
                    f"run function {step_func.id}"
                )
            else:
                ~ Execute().POSITIONED(Position3("^", "^", f"^{s_step}")).UNLESS(
                    lambda _c, b=block_obj: _c.block(b, Position3("~", "~", "~"))  # type: ignore
                ).IF(
                    lambda _c: _c.block(Block(Identifier.of("#minecraft", "replaceable")), Position3("~", "~", "~"))  # type: ignore
                ).RUN(step_func)

        ~ hit_func
        ~ step_func

        arr: CommandArray = CommandArray([])
        arr += dist_obj.add()
        arr += max_obj.add()
        arr += dist.set(0)
        arr += maximum.set(max_dist)
        arr += (
            Execute()
            .AS(TargetSelector.SELF)
            .AT(TargetSelector.SELF)
            .ANCHORED("eyes")
            .RUN(step_func)
        )
        return arr

    # -- target hit --------------------------------------------------------

    @staticmethod
    def on_target_hit(
        target: TargetSelector,
        hit: Command | CommandArray | Function | None = None,
        step_f: Command | CommandArray | None = None,
        step: float = 0.1,
        length: Range = Range.max(30),
    ) -> CommandArray:
        uid: int = _counter.get()
        s_step: str = RayCaster._step_str(step)
        max_dist: int = RayCaster._max_steps(length, step)

        dist_obj: ScoreboardObjective = Scoreboard.objective(f"__ray_d_{uid}", Text.literal(""), ObjectiveCriterion.DUMMY)
        max_obj: ScoreboardObjective = Scoreboard.objective(f"__ray_m_{uid}", Text.literal(""), ObjectiveCriterion.DUMMY)
        dist: ScoreboardPlayer = dist_obj.player(TargetSelector.SELF)
        maximum: ScoreboardPlayer = max_obj.player(TargetSelector.SELF)
        TAG = EntityTag(f"__raycast_{uid}")
        SOURCE_TAG = EntityTag(f"__raycast_source_{uid}")

        # target selector with virtual-volume + caster exclusion
        target_vol: TargetSelector = target.with_settings({
            "dx": 0,
            "tag": f"!{TAG}",
        })

        # hit_func: Function = Function(Identifier.of("temp", f"__raycast_{uid}_h"))
        # step_func: Function = Function(Identifier.of("temp", f"__raycast_{uid}_s"))
        hit_func: Function = Function()
        step_func: Function = Function()

        with hit_func:
            if hit is not None:
                if isinstance(hit, Function):
                    ~ hit.run({"source": f"@e[tag={SOURCE_TAG}, limit=1, sort=nearest]"})
                elif isinstance(hit, CommandArray):
                    ~ hit
                else:
                    ~ hit
            ~ Return.fail()

        with step_func:
            if step_f: ~ step_f
            ~ dist.add(1)
            ~ Execute().IF(
                lambda _c, d=dist, m=maximum: _c.score(d, ">", m)
            ).RUN(Return.fail())

            # entity hit — virtual volumes + return run
            ~ CustomCommand(
                f"execute positioned ~-.99 ~-.99 ~-.99 "
                f"as {target_vol} "
                f"positioned ~.99 ~.99 ~.99 "
                f"as @s[dx=0] "
                f"run return run function {hit_func.id}"
            )

            # wall check + recursion
            ~ CustomCommand(
                f"execute if block ~ ~ ~ #minecraft:replaceable "
                f"positioned ^ ^ ^{s_step} "
                f"run function {step_func.id}"
            )

        ~ hit_func
        ~ step_func

        arr = CommandArray([])
        arr += SOURCE_TAG.add(TargetSelector.SELF)
        arr += dist_obj.add()
        arr += max_obj.add()
        arr += dist.set(0)
        arr += maximum.set(max_dist)
        arr += CustomCommand(f"tag @s add {TAG}")
        arr += (
            Execute()
            .AS(TargetSelector.SELF)
            .AT(TargetSelector.SELF)
            .ANCHORED("eyes")
            .RUN(step_func)
        )
        arr += CustomCommand(f"tag @s remove {TAG}")
        arr += SOURCE_TAG.remove(TargetSelector.SELF)
        return arr

    # -- entity hit --------------------------------------------------------

    @staticmethod
    def on_entity_hit(
        entity: EntityType,
        hit: Command | CommandArray | None = None,
        step_f: Command | CommandArray | None = None,
        step: float = 0.1,
        length: Range = Range.max(30),
    ) -> CommandArray:
        target: TargetSelector = TargetSelector(
            "@e",
            TargetSelectorSettings(type=entity),
        )
        return RayCaster.on_target_hit(target, hit, step_f, step, length)