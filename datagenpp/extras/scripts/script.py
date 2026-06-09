from datagen.advancement.advancement import Advancement
from datagen.datapack.namespace import Namespace
from datagen.function.function import Function


class Script():
    def __init__(self) -> None:
        self.load = set[Function]()
        self.tick = set[Function]()
        self.functions = set[Function]()
        self.advancements = set[Advancement]()

    def add_function(self, function: Function) -> None:
        self.functions.add(function)

    def add_advancement(self, advancement: Advancement) -> None:
        self.advancements.add(advancement)

    def on_load(self, function: Function) -> None:
        self.load.add(function)

    def on_tick(self, function: Function) -> None:
        self.tick.add(function)

    def merge(self, namespace: Namespace) -> None:
        for function in self.load:
            function.id._namespace = namespace.name
            namespace.add_function(function)
            namespace.minecraft.load.add_value(function)
        for function in self.tick:
            function.id._namespace = namespace.name
            namespace.add_function(function)
            namespace.minecraft.tick.add_value(function)

        for function in self.functions:
            function.id._namespace = namespace.name
            namespace.add_function(function)

        for advancement in self.advancements:
            advancement.id._namespace = namespace.name
            namespace.add_advancement(advancement)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def __invert__(self):
        self.merge(Namespace.get_current_namespace())
        return self