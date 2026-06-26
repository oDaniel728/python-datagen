from typing import Any

from datagen.datapack.namespace import Namespace
from datagen.function.commands._data.datastorage import DataStorage, DataStorageValue
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.execute import Execute
from datagen.function.function import Function
from datagen.types.util.rtypes import TAny, TFunction, TIdentifier, TInteger, TPath, TString
from datagenpp.extras.packs.pack import Pack


class Builtins(Pack, name="dgbtns", description="Datagen++ built-in functions and commands"):

    class STORAGES:
        returns: DataStorageValue[dict[str, Any]]
        last_return: DataStorageValue[Any]
        cache: DataStorageValue[dict[str, Any]]
        letter_codes: DataStorageValue[dict[str, int]]
        code_letters: DataStorageValue[dict[int, str]]

    class FUNCTIONS:
        merge_string: Function[TString, TString]
        """
        Merges two strings and returns the result in the last_return.
        Args:
            0 (TString): The first string.
            1 (TString): The second string.
        Returns:
            last_return (TString): The merged string.
        """
        set_storage: Function[TIdentifier, TPath]
        """
        Sets a value in the specified storage.
        Args:
            0 (TIdentifier): The storage identifier.
            1 (TPath): The value to set.
        Returns:
            None: None
        """
        transfer_storage: Function[TIdentifier, TPath, TIdentifier, TPath]
        """
        Transfers a value from one storage to another.
        Args:
            0 (TIdentifier): The source storage identifier.
            1 (TPath): The source path in the source storage.
            2 (TIdentifier): The destination storage identifier.
            3 (TPath): The destination path in the destination storage.
        Returns:
            None: None
        """

        set_return: Function[TAny]
        """
        Sets the last return value.
        Args:
            0 (TAny): The value to set as the last return.
        Returns:
            None: None
        """
        set_cache: Function[TPath, TAny]
        """
        Sets a value in the cache.
        Args:
            0 (TPath): The cache key.
            1 (TAny): The value to set in the cache.
        Returns:
            None: None
        """
        clear_cache: Function
        """
        Clears the cache.
        Args:
            None: None
        Returns:
            None: None
        """

        load_chars: Function
        """
        Loads a predefined set of characters into the cache with their corresponding integer values.
        Args:
            None: None
        Returns:
            None: None
        """
        char_to_int: Function[TString]
        """
        Converts a character to its corresponding integer value.
        Args:
            0 (TString): The character to convert.
        Returns:
            last_return (int): The integer value of the character.
        """
        int_to_char: Function[int]
        """
        Converts an integer value to its corresponding character.
        Args:
            0 (int): The integer value to convert.
        Returns:
            last_return (TString): The character corresponding to the integer value.
        """

    class TAGS:
        ...

    def on_prepare(self) -> None:
        pass

    def on_register(self, ns: Namespace, mc: Namespace, tmp: Namespace) -> None:
        S, F, T = self.STORAGES, self.FUNCTIONS, self.TAGS
        S.returns = DataStorage(ns / "returns")['root']
        S.last_return = S.returns["0"]
        S.cache = DataStorage(ns / "cache")['root']

        with Function(ns / "string/merge") as F.merge_string: #
            _0 = F.merge_string["0"]
            _1 = F.merge_string["1"]
            
            ~ S.last_return.set(f"{_0}{_1}")
            ns += F.merge_string
            

        with Function(ns / "storage/set") as F.set_storage: #
            _0 = F.set_storage["0"]
            _1 = F.set_storage["1"]
            
            ~ S.cache[f"root.{_0}"].set(_1)
            ns += F.set_storage

        with Function(ns / "storage/transfer") as F.transfer_storage: #
            # _0: TIdentifier
            # _1: TPath
            # _2: TIdentifier
            # _3: TPath
            # _0 _1 -> _2 _3
            _0 = F.transfer_storage["0"]
            _1 = F.transfer_storage["1"]
            _2 = F.transfer_storage["2"]
            _3 = F.transfer_storage["3"]
            ~ DataStorage(_0)[_1].set(DataStorage(_2)[_3])
            ns += F.transfer_storage

        with Function(ns / "return") as F.set_return: #
            _0 = F.set_return["0"]
            
            ~ S.last_return.set(_0)
            ns += F.set_return
        
        with Function(ns / "cache/set") as F.set_cache: #
            _0 = F.set_cache["0"]
            _1 = F.set_cache["1"]
            
            ~ S.cache[f"{_0}"].set(_1)
            ns += F.set_cache

        with Function(ns / "cache/clear") as F.clear_cache: #
            ~ S.cache.set({})
            ns += F.clear_cache

        def _get_chars() -> list[tuple[str, int]]:
            upperletters = "abcdefghijklmnopqrstuvwxyz".upper()
            lowerletters = upperletters.lower()
            digits = "0123456789"
            symbols = r"""!@#$%^&*()-_=+[]{};:'",.<>/?\|`~"""
            whitespace = " \t\n\r"
            all_chars = lowerletters + upperletters + digits + symbols + whitespace
            return [(char, ord(char)) for char in all_chars]
        
        with Function(ns / "load/chars") as F.load_chars: #
            letters = S.cache["letter_codes"]
            codes = S.cache["code_letters"]
            letters.set({})
            codes.set({})
            for char, value in _get_chars():
                char = (char
                    .replace("\n", "\\\\n")
                    .replace("\r", "\\\\r")
                    .replace("\t", "\\\\t")
                    .replace("\\", "\\\\")
                    .replace("\"", "\\\"")
                )
                ~ letters[f"\"{char}\""].set(value)
                ~ codes[f"{value}"].set(char)
            self.letter_codes = letters
            self.code_letters = codes
            ns += F.load_chars
            mc.load += F.load_chars

        with Function(ns / "char/to_int") as F.char_to_int: #
            _0 = F.char_to_int["0"]
            ~ S.last_return.set(self.letter_codes[f"\"{_0}\""])
            ns += F.char_to_int

        with Function(ns / "char/to_char") as F.int_to_char: #
            _0 = F.int_to_char["0"]
            ~ S.last_return.set(self.code_letters[f"{_0}"])
            ns += F.int_to_char


    def on_build(self) -> None:
        pass