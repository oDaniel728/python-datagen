from datagen.extras.packs.pack import Pack
from functions.load import register_load


class MyPack(Pack, name="my_pack"):

    def register_functions(self) -> None:
        register_load(self)

    def on_register(self, ns, mc, tmp) -> None:
        self.logger.info("Hello, world!")

        self.register_functions()


def main() -> None:
    "entry point for the datagen package"
    MyPack()