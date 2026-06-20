from typing import Literal, TypedDict

from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands.execute import Execute
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.function.functionmacroargument import FunctionMacroArgument as FMA
from datagen.types.util.rtypes import TFunction, TIdentifier, TInteger, TPath
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.scoreboard.objective import ScoreboardObjective


class Tests():
    loopStart: Function[TInteger, TInteger, TInteger, TIdentifier]
    """
    A minecraft function wich executes a loop from start to end with 
    a given step, executing a function in each iteration.

    ## Args:
        _params in called function_
        **start** : *TInteger* <br> The starting index of the loop
        **end** : *TInteger* <br> The ending index of the loop
        **step** : *TInteger* <br> The step of the loop
        **function** : *TIdentifier[Function]* <br> The function to be executed in each iteration

    ## Context:
        _params inside function_
        **i** : *TInteger* <br> The current iteration index
        **min** : *TInteger* <br> The minimum index of the loop
        **max** : *TInteger* <br> The maximum index of the loop
        **step** : *TInteger* <br> The step of the loop
        **function** : *TIdentifier[Function]* <br> The function to be executed in each iteration
        
    Examples:
    ```python

    with~ Function(ns / "some/function/here) as f:
        i = f['i']
        min = f['min']
        max = f['max']
        step = f['step']
        function = f['function']

        ~ Say(f"Iteration {i} inside the range {min}..{max} with {step} steps running {function}")

    ~ Tests.loopStart(1, 10, 1, f)
    # min, max, function = 1, 10, f
    # for i in min..max: function(i, min, max, step)
    ```
    """


    def __init__(self) -> None:
        self.dp = DataPack("tests", "")
        self.ns : Namespace
        self.mc : Namespace
        self.tmp: Namespace
        
        self.prepare()
        self.register()
        self.build()

    def prepare(self) -> None: 
        self.ns = Namespace(self.dp.name)
        self.mc = Namespace.minecraft()
        self.tmp = Namespace.temp()

    def register(self) -> None: 
        self.dp += self.ns, self.mc, self.tmp
        ns, mc, tmp = self.ns, self.mc, self.tmp

        loop = "__loop"
        # region for loop range
        def register_iter_loop():
            with~ Function(ns / f"{loop}/iter/start") as lstart:
                # _0, '0' : start
                # _1, '1' : end
                # _2, '2' : step
                # _3, '3' : function
                _0: FMA[TInteger] = lstart['0']
                _1: FMA[TInteger] = lstart['1']
                _2: FMA[TInteger] = lstart['2']
                _3: FMA[TIdentifier] = lstart['3']

                obj = ~ ScoreboardObjective(f"{loop}i{_0}to{_1}in{_2}", LiteralText("Loop Counter"))
                ~ obj.rset({
                    "start": _0,
                    "end": _1,
                    "step": _2,
                    "current": obj['start'],
                })

                args = DataStorage(ns / f"{loop}/iter/step/args")
                ~ args["function"].set(_3)
                
                ~ RunFunction(ns / f"{loop}/iter/step", args)

            args = DataStorage(ns / f"{loop}/iter/step/args")

            with~ Function(ns / f"{loop}/iter/step") as lstep:
                _FUNC = lstep['function']
                ~ obj['current'].add(obj['step'])
                with AnonymousFunction() as _a:
                    ~ args.rset({
                        "i": obj['current'],
                        "min": obj['start'],
                        "max": obj['end'],
                        "step": obj['step'],
                    })

                    ~ RunFunction(_FUNC, args)
                    ~ lstep.run(args)
                tmp.add(_a)
                    
                ~ (
                    Execute()
                    .IF(lambda b: 
                        b.score(obj['current'], "<=", obj['end'])
                    )
                    .RUN(_a.run(args))
                )
            Tests.loopStart = lstart
        register_iter_loop() # Tests.loopStart exists!
        # endregion

    def build(self) -> None:
        self.dp.build()
