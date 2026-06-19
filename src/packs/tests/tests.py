from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._return import Return
from datagen.function.commands.execute import Execute
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.minecraft.text._components import LiteralText
from datagen.utils.scoreboard.objective import ScoreboardObjective
from datagen.utils.scoreboard.player import ScoreboardPlayer


class Tests():
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

        with~ Function(ns / "loop/main") as lmain:
            i = lmain['i']
            min = lmain['min']
            max = lmain['max']
            step = lmain['step']
            ~ Say(f"Iteração {i} em {min}..{max} com passo {step}")
        
        with~ Function(ns / "loop/start") as lstart:
            # _0, '0' : start
            # _1, '1' : end
            # _2, '2' : step
            # _3, '3' : function
            _0 = lstart['0']
            _1 = lstart['1']
            _2 = lstart['2']
            _3 = lstart['3']

            obj = ~ ScoreboardObjective("loop", LiteralText("Loop Counter"))
            ~ obj.rset({
                "start": _0,
                "end": _1,
                "step": _2,
                "current": obj['start'],
            })

            args = DataStorage(ns / "loop/step/args")
            ~ args["function"].set(_3)
            
            ~ RunFunction(ns / "loop/step", args)

        args = DataStorage(ns / "loop/step/args")

        with~ Function(ns / "loop/step") as lstep:
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
            tmp += _a
                
            ~ (
                Execute()
                .IF(lambda b: 
                    b.score(obj['current'], "<=", obj['end'])
                )
                .RUN(_a.run(args))
            )



    def build(self) -> None:
        self.dp.build()
