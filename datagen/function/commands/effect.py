from typing import Literal, overload

from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.types.exceptions.preventionexception import PreventionException
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.repr.status_effect import StatusEffect


class Effect():
    _TInfinite = Literal["infinite"]
    @overload
    @staticmethod
    def clear() -> CustomCommand: ...

    @overload
    @staticmethod
    def clear(target: TargetSelector, /) -> CustomCommand: ...

    @staticmethod
    def clear(target: TargetSelector | None = None, /) -> CustomCommand:
        return CustomCommand(f"effect clear {target or '@s'}")
    
    @overload
    @staticmethod
    def give(
        target: TargetSelector,
        effect: StatusEffect,
        /,
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def give(
        target: TargetSelector,
        effect: StatusEffect,
        seconds: int | _TInfinite,
        /,
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def give(
        target: TargetSelector,
        effect: StatusEffect,
        seconds: int,
        amplifier: int,
        /,
    ) -> CustomCommand: ...
    @overload
    @staticmethod
    def give(
        target: TargetSelector,
        effect: StatusEffect,
        seconds: int,
        amplifier: int,
        hideParticles: bool,
        /,
    ) -> CustomCommand: ...

    @staticmethod
    def give(
        target: TargetSelector,
        effect: StatusEffect,
        seconds: int | _TInfinite = 30,
        amplifier: int = 0,
        hideParticles: bool = False,
        /,
    ) -> CustomCommand:
        if amplifier < 0:
            raise PreventionException("Amplifier must be greater than or equal to 0.")
        elif amplifier > 255:
            raise PreventionException("Amplifier must be less than or equal to 255.")
        
        if isinstance(seconds, int) and seconds < 0:
            raise PreventionException("Seconds must be greater than or equal to 0.")

        return CustomCommand(
            f"effect give {target} {effect} {seconds} {amplifier} {'true' if hideParticles else 'false'}"
        )