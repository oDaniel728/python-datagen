from typing import Literal, overload

from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.time import Time
from datagen.types.exceptions.preventionexception import PreventionException


class Weather():
    _TWeather = Literal["clear", "rain", "thunder"]
    @overload
    def __new__(cls, weather: _TWeather, /) -> CustomCommand: ...
    @overload
    def __new__(cls, weather: _TWeather, duration: int, unit: Time._TUnit, /) -> CustomCommand: ...
    
    def __new__(cls, weather: _TWeather, duration: int | None = None, unit: Time._TUnit | None = None, /) -> CustomCommand:
        if weather not in ["clear", "rain", "thunder"]:
            raise PreventionException(f"Invalid weather type: {weather}. Valid types are 'clear', 'rain', and 'thunder'.")
        if duration and unit:
            if duration < 0:
                raise PreventionException("Duration must be a non-negative integer.")
            return CustomCommand("weather", f"{weather} {duration}{unit[0]}")
        return CustomCommand("weather", weather)

    @overload
    @staticmethod
    def clear() -> CustomCommand: ...
    @overload
    @staticmethod
    def clear(
        duration: int,
        unit: Time._TUnit,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def clear(duration: int | None = None, unit: Time._TUnit | None = None, /) -> CustomCommand:
        return Weather("clear", duration, unit) # type: ignore
    
    @overload
    @staticmethod
    def rain() -> CustomCommand: ...
    @overload
    @staticmethod
    def rain(
        duration: int,
        unit: Time._TUnit,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def rain(duration: int | None = None, unit: Time._TUnit | None = None, /) -> CustomCommand:
        return Weather("rain", duration, unit) # type: ignore
    
    @overload
    @staticmethod
    def thunder() -> CustomCommand: ...
    @overload
    @staticmethod
    def thunder(
        duration: int,
        unit: Time._TUnit,
        /
    ) -> CustomCommand: ...

    @staticmethod
    def thunder(duration: int | None = None, unit: Time._TUnit | None = None, /) -> CustomCommand:
        return Weather("thunder", duration, unit) # type: ignore