from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._return import Return
from datagen.function.commands.execute import Execute
from datagen.function.function import Function
from datagen.utils.scoreboard.objective import ScoreboardObjective


class BoolUtils():
    def __init__(self) -> None:
        self.dp = DataPack("bool_utils", "A datapack with boolean utilities")
        self.ns : Namespace
        self.mc : Namespace
        
        self.prepare()
        self.register()
        self.build()

    def prepare(self) -> None: 
        self.ns = Namespace("bool_utils")
        self.mc = Namespace.minecraft

    def register(self) -> None: 
        self.dp += self.ns, self.mc
        ns, mc = self.ns, self.mc

        with~ Function(ns / "op/not") as op_not:
            # if _0 == 1 return 0
            # if _0 == 0 return 1
            _0 = op_not['0', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(1)
            ~ value.remove(_0)
            ~ Return.score(value)

        with~ Function(ns / "op/and") as op_and:
            # if _0 == 1 and _1 == 1 return 1 else return 0
            _0 = op_and['0', int]
            _1 = op_and['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']
            ~ value.set(1)
            ~ value.multiply(_0)
            ~ value.multiply(_1)
            ~ Return.score(value)

        with~ Function(ns / "op/or") as op_or:
            # if _0 == 1 or _1 == 1 return 1 else return 0
            _0 = op_or['0', int]
            _1 = op_or['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']

            other = (~ ScoreboardObjective.TEMP)['__other']
            ~ other.set(1)
            
            ~ value.set(0)
            ~ value.add(_0)
            ~ value.add(_1)

            ~ value.min(other)

            ~ Return.score(value)

        with~ Function(ns / "op/xor") as op_xor:
            # if _0 == 1 and _1 == 0 return 1
            # if _0 == 0 and _1 == 1 return 1
            # else return 0
            _0 = op_xor['0', int]
            _1 = op_xor['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']

            other = (~ ScoreboardObjective.TEMP)['__other']
            ~ other.set(1)
            
            ~ value.set(0)
            ~ value.add(_0)
            ~ value.add(_1)

            ~ value.min(other)

            # if both are 1, set to 0
            both = (~ ScoreboardObjective.TEMP)['__both']
            ~ both.set(1)
            ~ both.multiply(_0)
            ~ both.multiply(_1)

            ~ value.remove(both)

            ~ Return.score(value)

        with~ Function(ns / "if/value_check") as if_value_check:
            # if _0 == _1 return 1 else return 0
            _0 = if_value_check['0', int]
            _1 = if_value_check['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']

            other = (~ ScoreboardObjective.TEMP)['__other']
            ~ other.set(1)
            
            ~ value.set(0)
            ~ value.add(_0)
            ~ value.remove(_1)

            ~ value.min(other)

            ~ Return.score(value)

        with~ Function(ns / "if/value_check_not") as if_value_check_not:
            # return 1 if _0 != _1 else 0
            # (equivalent to XOR for boolean values)
            _0 = if_value_check_not['0', int]
            _1 = if_value_check_not['1', int]
            value = (~ ScoreboardObjective.TEMP)['__result']

            other = (~ ScoreboardObjective.TEMP)['__other']
            ~ other.set(1)

            ~ value.set(0)
            ~ value.add(_0)
            ~ value.add(_1)

            ~ value.min(other)

            both = (~ ScoreboardObjective.TEMP)['__both']
            ~ both.set(1)
            ~ both.multiply(_0)
            ~ both.multiply(_1)

            ~ value.remove(both)

            ~ Return.score(value)

    def build(self) -> None:
        self.dp.build()
