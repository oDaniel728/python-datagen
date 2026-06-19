
from datagen.datapack.datapack import DataPack
from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._return import Return
from datagen.function.commands.execute import Execute
from datagen.function.commands.say import Say
from datagen.function.function import Function
from datagen.utils.scoreboard.objective import ScoreboardObjective
from utils._version import version


class FuncUtils():

    def get_chars(self) -> str:
        letters = "aãâáàbcçĉćdeẽêéèfgĝǵhiĩîíìjĵklĺmḿnñńǹoõôóòpṕqrŕsŝśtuũûúùvṽǜwŵẃẁxyỹŷýỳzẑź"
        uppers = letters.upper()
        digits = "0123456789"
        others = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        return letters + uppers + digits + others
    
    def get_mapped_chars(self) -> dict[int, str]:
        chars = self.get_chars()
        return {i: char for i, char in enumerate(chars)}

    def __init__(self) -> None:
        self.dp = ~ DataPack("func_utils", "A datapack with function utilities")
        self.ns : Namespace
        self.mc : Namespace
        
        self.prepare()
        self.register()
        self.build()

    def prepare(self) -> None: 
        self.ns = ~ Namespace(self.dp.name)
        self.mc = ~ Namespace.minecraft()

    def register(self) -> None: 
        ns, mc = self.ns, self.mc

        ns += version("1.0.0").encapsulate("version")

        with~ Function(ns / "char/__load/load_chars") as load_chars:
            int_to_charmap = DataStorage(ns / "utils/int_to_character_map")
            char_to_intmap = DataStorage(ns / "utils/character_to_int_map")

            rmap = {
                "\n": "\\n",
                "\\": "\\\\",
                "\"": "\\\"",
            }
            def _rpl(t: str) -> str:
                for k, v in rmap.items():
                    t = t.replace(k, v)
                return t
            def _getmapped() -> dict[int, str]:
                return {
                    i: _rpl(char) 
                    for i, char in self.get_mapped_chars().items()
                }
            ~ int_to_charmap.rset({
                f"{i}": char 
                for i, char in _getmapped().items()
            })
            ~ char_to_intmap.rset({
                f"\"{_rpl(char)}\"": i
                for i, char in _getmapped().items()
            })

        with~ Function(ns / "char/load") as load:
            ~ load_chars.run()
            mc.load += load

        with~ Function(ns / "char/to_int") as char_to_int:
            _0 = char_to_int['0', str]
            ~ Return.run(char_to_intmap.get(_0))

        with~ Function(ns / "char/to_char") as int_to_char:
            _0 = int_to_char['0', str]
            ~ Return.run(int_to_charmap.get(_0))


    def build(self) -> None:
        self.dp.build()
