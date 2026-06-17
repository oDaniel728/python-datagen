from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands._return import Return
from datagen.function.function import Function
from datagen.utils.scoreboard.objective import ScoreboardObjective


class MathUtils():
    def __init__(self) -> None:
        self.dp = DataPack("math_utils", "A datapack with math utilities")
        self.ns : Namespace
        self.mc : Namespace
        
        self.prepare()
        self.register()
        self.build()

    def prepare(self) -> None: 
        self.ns = Namespace("math_utils")
        self.mc = Namespace.minecraft

    def register(self) -> None: 
        self.dp += self.ns, self.mc
        ns, mc = self.ns, self.mc
        
        with~ Function(ns / "op/sum") as op_sum:
            _0 = op_sum['0', int]
            _1 = op_sum['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(_0)
            ~ value.add(_1)
            ~ Return.score(value)

        with~  Function(ns / "op/sub") as op_sub:
            _0 = op_sub['0', int]
            _1 = op_sub['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(_0)
            ~ value.remove(_1)
            ~ Return.score(value)

        with~ Function(ns / "op/mul") as op_mul:
            _0 = op_mul['0', int]
            _1 = op_mul['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(_0)
            ~ value.multiply(_1)
            ~ Return.score(value)

        with~ Function(ns / "op/div") as op_div:
            _0 = op_div['0', int]
            _1 = op_div['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(_0)
            ~ value.divide(_1)
            ~ Return.score(value)

    def build(self) -> None:
        self.dp.build()
