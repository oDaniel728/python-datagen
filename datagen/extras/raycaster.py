import math
from typing import overload

from datagen.function.commands.command import Command
from datagen.function.commands.commandarray import CommandArray
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.execute import Execute
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.targetselectorsettings import TargetSelectorSettings
from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.position3 import Position3
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagen.utils.scoreboard.player import ScoreboardPlayer


class RayCaster():
    """Generates inline raycast commands for Minecraft datapacks.

    Each method returns a ``CommandArray`` that checks positions along
    the executor's looking direction and runs *c* on the first match.

    The generated commands use ``positioned ^ ^ ^`` (local coordinates),
    ``execute store success score`` to stop at the first hit, and the
    project's ``temp`` scoreboard objective for the hit flag.

    Examples:

        >>> with Function(Identifier.of("my_pack:shoot")) as f:
        ...     ~ RayCaster.on_block_hit(
        ...         block=Identifier.of("minecraft:stone"),
        ...         c=Execute().RUN(Say("Found stone!")),
        ...         step=1.0,
        ...         length=Range.max(64),
        ...     )
    """

    @staticmethod
    def _fmt_step(d: float) -> str:
        """Format a step distance for use in ``^ ^ ^<value>``."""
        if d == math.floor(d):
            return str(int(d))
        return f"{d:g}"

    @staticmethod
    def _steps(step: float, length: Range) -> list[str]:
        _max: int | None = length.end
        max_len: float = float(_max) if _max is not None else 64.0
        if step <= 0 or max_len <= 1e-12:
            return []
        steps: list[str] = []
        d: float = step
        while d <= max_len + 1e-9:
            steps.append(RayCaster._fmt_step(round(d, 6)))
            d += step
        return steps

    @staticmethod
    def _add_header(arr: CommandArray) -> tuple[ScoreboardPlayer, Command]:
        """Append objective-creation and flag-reset to *arr*.

        Returns ``(hit_flag, hit_cmd)`` where *hit_flag* is the
        ``ScoreboardPlayer`` backing the stop-on-hit logic and
        *hit_cmd* is a ``Command`` that sets that flag to ``1``.
        """
        hit_flag: ScoreboardPlayer = ScoreboardObjective.TEMP.player("__ray_hit")
        arr += ScoreboardObjective.TEMP.add()
        arr += hit_flag.set(0)
        return hit_flag, hit_flag.set(1)

    @overload
    @staticmethod
    def on_block_hit(
        block: Identifier,
        c: Command | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray: ...

    @overload
    @staticmethod
    def on_block_hit(
        block: Block,
        c: Command | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray: ...

    @staticmethod
    def on_block_hit(
        block: Identifier | Block,
        c: Command | None = None,
        step: float = 1.0,
        length: Range = Range.max(30),
    ) -> CommandArray:
        """Raycast until a specific block is hit.

        The execution position at the moment *c* runs is the hit block's
        position, so ``~ ~ ~`` inside *c* refers to the block itself.

        Args:
            block: Block identifier (type-only) or ``Block`` instance
                (includes block state / NBT data).  When a ``Block`` is
                given, the full block state (``[state]``) and block
                entity data (``{...}``) are also checked at runtime.
            c: Command to execute on hit.  If ``None`` the hit is still
                detected and stops further checks.
            step: Distance in blocks between each check.
            length: Maximum raycast distance.
        """
        arr = CommandArray([])
        hit_flag, hit_cmd = RayCaster._add_header(arr)

        block_obj: Block = Block(block) if isinstance(block, Identifier) else block
        settings = block_obj.settings  # type: ignore
        has_state: bool = bool(settings.get_block_state()) or bool(settings.get_block_entity_data())  # type: ignore
        block_str: str = str(block_obj) if has_state else str(block_obj.id)
        action: Command = c if c is not None else hit_cmd
        flag_ref: str = f"{hit_flag.name} {hit_flag.objective}"

        for d in RayCaster._steps(step, length):
            if has_state:
                arr += CustomCommand(
                    f"execute if score {flag_ref} matches 0 "
                    f"store success score {flag_ref} "
                    f"as @s at @s anchored eyes positioned ^ ^ ^{d} "
                    f"if block ~ ~ ~ {block_str} "
                    f"run {action.raw()}"
                )
            else:
                arr += (Execute()
                    .IF(lambda _c, f=hit_flag: _c.score(f, "matches", 0))  # type: ignore
                    .STORE("success", "score", hit_flag)
                    .AS(TargetSelector.SELF)
                    .AT(TargetSelector.SELF)
                    .ANCHORED("eyes")
                    .POSITIONED(Position3("^", "^", f"^{d}"))
                    .IF(lambda _c, b=block_obj: _c.block(b, Position3("~", "~", "~")))  # type: ignore
                    .RUN(action)
                )

        return arr


    @staticmethod
    def on_target_hit(
        target: TargetSelector,
        c: Command | None = None,
        step: float = 0.1,
        length: Range = Range.max(30),
        radius: float = 0.5,
    ) -> CommandArray:
        """Raycast until an entity matching *target* is within *radius*.

        The *target* selector is augmented with a ``distance`` filter
        set to ``..<radius>`` so that only entities within that radius
        of each check point are considered.

        Args:
            target: Target selector to match (e.g. nearest player,
                all entities with a tag, etc.).
            c: Command to execute on hit.
            step: Distance between each check.
            length: Maximum raycast distance.
            radius: Detection radius at each check point.
        """
        arr = CommandArray([])
        hit_flag, hit_cmd = RayCaster._add_header(arr)

        action: Command = c if c is not None else hit_cmd
        target_filtered: TargetSelector = target.with_settings(
            {"distance": f"..{radius}"}
        )

        for d in RayCaster._steps(step, length):
            arr += (Execute()
                .IF(lambda _c, f=hit_flag: _c.score(f, "matches", 0))  # type: ignore
                .STORE("success", "score", hit_flag)
                .AS(TargetSelector.SELF)
                .AT(TargetSelector.SELF)
                .ANCHORED("eyes")
                .POSITIONED(Position3("^", "^", f"^{d}"))
                .IF(lambda _c, t=target_filtered: _c.entity(t))  # type: ignore
                .RUN(action)
            )

        return arr

    @staticmethod
    def on_entity_hit(
        entity: EntityType,
        c: Command | None = None,
        step: float = 0.1,
        length: Range = Range.max(30),
        radius: float = 0.5,
    ) -> CommandArray:
        """Raycast until an entity of the given type is within *radius*.

        A convenience wrapper that builds ``@e[type=<entity>]``
        internally and delegates to ``on_target_hit``.

        Args:
            entity: The entity type to look for.
            c: Command to execute on hit.
            step: Distance between each check.
            length: Maximum raycast distance.
            radius: Detection radius at each check point.
        """
        target: TargetSelector = TargetSelector(
            "@e",
            TargetSelectorSettings(type=entity),
        )
        return RayCaster.on_target_hit(target, c, step, length, radius)
