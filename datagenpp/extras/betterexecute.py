from typing import Callable, Self

from typing import overload

from datagen.function.commands.command import Command
from datagen.function.commands.execute import Execute, _ConditionBuilder, IDontCare
from datagen.function.function import Function

class BetterExecute(Execute):
    def __init__(self):
        super().__init__()
        self._commands_before = list[Command]()
        self._commands_after = list[Command]()
    
    @overload
    def CONDITION(self, 
        condition: Callable[[_ConditionBuilder], IDontCare], 
        then: Command | Function,
        /
    ) -> "Self":
        ...
    @overload
    def CONDITION(self, 
        condition: Callable[[_ConditionBuilder], IDontCare], 
        then: Command | Function, 
        unless: Command | Function,
        /
    ) -> "Self":
        ...

    def CONDITION(self, condition: Callable[[_ConditionBuilder], IDontCare], then: Command | Function, unless: Command | Function | None = None, /):
        self._check_seal()
        self._commands_before.append(self.copy().IF(condition).RUN(then))
        if unless is not None:
            self._commands_before.append(self.copy().UNLESS(lambda x: condition(x)).RUN(unless))
        self._chunks = []
        self._sealed = True
        return self
    
    def to_string(self) -> str:
        return "\n".join(
            [cmd.to_string() for cmd in self._commands_before] +
            [super().to_string() if self._chunks else ''] +
            [cmd.to_string() for cmd in self._commands_after]
        )

