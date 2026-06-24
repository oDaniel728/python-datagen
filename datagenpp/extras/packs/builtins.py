from datagen.datapack.namespace import Namespace
from datagen.function.commands._data.datastorage import DataStorage, DataStorageValue
from datagen.function.function import Function
from datagen.types.util.rtypes import TAny, TIdentifier, TPath, TString
from datagenpp.extras.packs.pack import Pack


class Builtins(Pack, name="dgbtns", description="Datagen++ built-in functions and commands"):

    # Storages
    returns: DataStorage
    last_return: DataStorageValue
    cache: DataStorage

    # Functions
    merge_string: Function[TString, TString]
    """
    Merges two strings and returns the result in the last_return.
    Args:
        0: The first string.
        1: The second string.
    Returns:
        last_return: The merged string.
    """
    set_storage: Function[TIdentifier, TPath]
    """
    Sets a value in the specified storage.
    Args:
        0: The storage identifier.
        1: The value to set.
    Returns:
        None: None
    """
    equals: Function[TAny, TAny]
    """
    Compares two values and returns true if they are equal, false otherwise.
    Args:
        0: The first value.
        1: The second value.
    Returns:
        last_return: True if the values are equal, false otherwise.
    """

    def on_prepare(self) -> None:
        pass

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        self.returns = DataStorage(ns / "returns")
        self.last_return = self.returns["0"]
        self.cache = DataStorage(ns / "cache")

        with Function(ns / "merge_string") as self.merge_string:
            _0 = self.merge_string["0"]
            _1 = self.merge_string["1"]
            
            ~ self.last_return.set(f"{_0}{_1}")
            ns += self.merge_string
            

        with Function(ns / "set_storage") as self.set_storage:
            _0 = self.set_storage["0"]
            _1 = self.set_storage["1"]
            
            ~ self.cache[_0].set(_1)
            ns += self.set_storage

    def on_build(self) -> None:
        pass