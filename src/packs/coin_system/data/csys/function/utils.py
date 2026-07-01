from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands.execute import Execute
from datagen.function.commands.random import Random
from datagen.function.commands.runfunction import RunFunction


class UtilsFunctions():

    @staticmethod
    def register_run_at_random_position(ns: Namespace, tmp: Namespace) -> None:
        with ns.create_function("utils/run_at_random_position") as run_at_random_position:
            _0 = run_at_random_position.arg("0", int)
            _1 = run_at_random_position.arg("1", int)
            _2 = run_at_random_position.arg("2", int)
            _3 = run_at_random_position.arg("3", int)
            _4 = run_at_random_position.arg("4", int)
            _5 = run_at_random_position.arg("5", int)
            _6 = run_at_random_position.arg("6", str)
            with AnonymousFunction() as a3:
                x = a3['x']
                y = a3['y']
                z = a3['z']
                func = a3['func']
                ~ (
                    Execute()
                        .RUN(RunFunction(func, {'x': x, 'y': y, 'z': z}))
                )
                tmp += a3

            ARGS = DataStorage(tmp / "a3args")
            ~ ARGS.rset({
                "x": Random.value(f"{_0}..{_1}"),
                "y": Random.value(f"{_2}..{_3}"),
                "z": Random.value(f"{_4}..{_5}"),
                "func": _6
            })

            ~ a3.run(ARGS)
