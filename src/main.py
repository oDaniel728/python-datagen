from datagen.extras.packs.pack import Pack
from functions.load import register_load
from functions.other import register_other
from functions.test import register_test


class MyPack(Pack, name="my_pack"):

    def register_functions(self) -> None:
        register_load(self)
        register_other(self)
        register_test(self)

    def on_register(self, ns, mc, tmp) -> None:
        self.logger.info("Hello, world!")

        self.register_functions()

def main() -> None:
    "entry point for the datagen package"
    MyPack()