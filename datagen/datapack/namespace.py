from pathlib import Path
from typing import TYPE_CHECKING
from typing import final
from uuid import uuid4
from typing_extensions import Self

from datagen.function.function import Function
from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.logger import Logger

if TYPE_CHECKING:
    from datagen.predicate.predicate import Predicate
    from datagen.recipes.recipe import Recipe

@final
class Namespace():
    minecraft: Namespace
    temp: Namespace

    instances = dict[str, "Self"]()
    
    def __new__(cls, name: str) -> Self:
        if name in cls.instances:
            return cls.instances[name]
        else:
            ns = super().__new__(cls)
            cls.instances[name] = ns
            return ns

    @staticmethod
    def get(name: str | Identifier) -> "Namespace":
        if isinstance(name, Identifier):
            name = name._namespace

        if name in Namespace.instances:
            return Namespace.instances[name]
        else:
            ns = Namespace(name)
            Namespace.instances[name] = ns
            return ns

    def __init__(self, name: str):
        self.name = name

        self.logger = Logger(name)

        self.functions = set[Function]()
        self.tags = set[Tag]()
        self.predicates = set["Predicate"]()
        self.recipes = set["Recipe"]()

    def identifier(self, path: str) -> Identifier:
        return Identifier.from_string(f"{self.name}:{path}")
    
    def add(self, obj: Function | Tag | "Predicate") -> Self:
        from datagen.predicate.predicate import Predicate

        if isinstance(obj, Function):
            return self.add_function(obj)
        elif isinstance(obj, Tag):
            return self.add_tag(obj)
        elif isinstance(obj, Predicate):
            return self.add_predicate(obj)
        else:
            raise TypeError(f"Object of type '{type(obj)}' is not a Function, Tag or Predicate")
    
    def add_function(self, function: Function) -> Self:
        self.logger.info(f"Adding function '{function.id._path}' to namespace '{self.name}'")
        function.namespace = self
        self.functions.add(function)
        return self
    
    def add_tag(self, tag: Tag) -> Self:
        self.logger.info(f"Adding tag '{tag.id._path}' to namespace '{self.name}'")
        tag.namespace = self
        self.tags.add(tag)
        return self

    def add_predicate(self, predicate: "Predicate") -> Self:
        self.logger.info(f"Adding predicate '{predicate.id._path}' to namespace '{self.name}'")
        predicate.namespace = self
        self.predicates.add(predicate)
        return self

    def add_recipe(self, recipe: "Recipe") -> Self:
        self.logger.info(f"Adding recipe '{recipe.id._path}' to namespace '{self.name}'")
        recipe.namespace = self
        recipe.id._namespace = self.name
        self.recipes.add(recipe)
        return self
    
    def add_recipes(self, *recipes: "Recipe") -> Self:
        for recipe in recipes:
            self.add_recipe(recipe)
        return self
    
    def add_tags(self, *tags: Tag) -> Self:
        for tag in tags:
            self.add_tag(tag)
        return self
    
    def build_functions(self, base: Path):
        Logger.start_task(f"Building functions in namespace '{self.name}'")
        for function in self.functions:
            self.logger.info(f"Building function '{function.id._path}' in namespace '{self.name}'")
            f = function.to_file()
            f.build(base)
        Logger.end_task(f"Building functions in namespace '{self.name}'")

    def build_tags(self, base: Path):
        Logger.start_task(f"Building tags in namespace '{self.name}'")
        for tag in self.tags:
            self.logger.info(f"Building tag '{tag.id._path}' in namespace '{self.name}'")
            f = tag.to_file()
            f.build(base)
        Logger.end_task(f"Building tags in namespace '{self.name}'")

    def build_predicates(self, base: Path):
        Logger.start_task(f"Building predicates in namespace '{self.name}'")
        for predicate in self.predicates:
            self.logger.info(f"Building predicate '{predicate.id._path}' in namespace '{self.name}'")
            f = predicate.to_file()
            f.build(base)
        Logger.end_task(f"Building predicates in namespace '{self.name}'")

    def build_recipes(self, base: Path):
        Logger.start_task(f"Building recipes in namespace '{self.name}'")
        for recipe in self.recipes:
            self.logger.info(f"Building recipe '{recipe.id._path}' in namespace '{self.name}'")
            f = recipe.to_file()
            f.build(base)
        Logger.end_task(f"Building recipes in namespace '{self.name}'")

    def build(self, base: Path):
        Logger.start_task(f"Building namespace '{self.name}'")
        self.build_functions(base)
        self.build_tags(base)
        self.build_predicates(base)
        self.build_recipes(base)
        Logger.end_task(f"Building namespace '{self.name}'")

    def __truediv__(self, path: str) -> Identifier:
        return self.identifier(path)

Namespace.minecraft = Namespace("minecraft")
Namespace.temp = Namespace(f"temp")