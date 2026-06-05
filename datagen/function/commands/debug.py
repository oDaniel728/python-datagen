
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.function import Function
from datagen.utils.minecraft.identifier import Identifier


class Debug():
    @staticmethod
    def start() -> CustomCommand:
        return CustomCommand("debug start")
    
    @staticmethod
    def stop() -> CustomCommand:
        return CustomCommand("debug stop")
    
    @staticmethod
    def function(func: Function | Identifier) -> CustomCommand:
        func_id = func.id if isinstance(func, Function) else func
        return CustomCommand(f"debug function {func_id.to_string()}")
