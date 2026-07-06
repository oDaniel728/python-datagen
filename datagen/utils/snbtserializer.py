from __future__ import annotations

from typing import Any
import re

from datagen.extras.color import Color
from datagen.function.functionmacroargument import FunctionMacroArgument
from datagen.types.util.holder import Holder
from datagen.types.util.min import Range
from datagen.utils.json_encoder import dumps
from datagen.utils.minecraft.identifier import Identifier


# ============================================================
# NBT ARRAY TYPES
# ============================================================

class ByteArray(list[int]):
    pass


class IntArray(list[int]):
    pass


class LongArray(list[int]):
    pass


# ============================================================
# SERIALIZER
# ============================================================

class SNBTSerializer:
    """
    SNBT serializer/deserializer compatível com
    Minecraft Java 1.21.1

    Suporta:
    - compounds {}
    - lists []
    - byte arrays [B;]
    - int arrays [I;]
    - long arrays [L;]
    - strings
    - byte/short/int/long
    - float/double
    - booleans
    """

    # ========================================================
    # SERIALIZE
    # ========================================================

    @staticmethod
    def serialize(value: dict[str, Any]) -> str:
        return SNBTSerializer._serialize_value(value)

    @staticmethod
    def _serialize_value(value: Any) -> str:

        # ----------------------------------------------------
        # COMPOUND
        # ----------------------------------------------------

        if isinstance(value, dict):
            items = []

            for k, v in value.items():
                items.append(
                    f"{SNBTSerializer._escape_key(k)}:"
                    f"{SNBTSerializer._serialize_value(v)}"
                )

            return "{" + ",".join(items) + "}"

        # ----------------------------------------------------
        # BYTE ARRAY
        # ----------------------------------------------------

        elif isinstance(value, ByteArray):
            return (
                "[B;"
                + ",".join(f"{x}b" for x in value)
                + "]"
            )

        # ----------------------------------------------------
        # INT ARRAY
        # ----------------------------------------------------

        elif isinstance(value, IntArray):
            return (
                "[I;"
                + ",".join(str(x) for x in value)
                + "]"
            )

        # ----------------------------------------------------
        # LONG ARRAY
        # ----------------------------------------------------

        elif isinstance(value, LongArray):
            return (
                "[L;"
                + ",".join(f"{x}l" for x in value)
                + "]"
            )

        # ----------------------------------------------------
        # LIST
        # ----------------------------------------------------

        elif isinstance(value, list):
            return (
                "["
                + ",".join(
                    SNBTSerializer._serialize_value(v)
                    for v in value
                )
                + "]"
            )

        # ----------------------------------------------------
        # IDENTIFIER
        # ----------------------------------------------------

        elif isinstance(value, Identifier):
            return f'"{value.to_string()}"'

        # ----------------------------------------------------
        # BOOLEAN
        # ----------------------------------------------------

        elif isinstance(value, bool):
            return "1b" if value else "0b"

        # ----------------------------------------------------
        # INTEGER
        # ----------------------------------------------------

        elif isinstance(value, int):
            return str(value)

        # ----------------------------------------------------
        # FLOAT
        # ----------------------------------------------------

        elif isinstance(value, float):
            return f"{value}d"

        # ----------------------------------------------------
        # STRING
        # ----------------------------------------------------

        elif isinstance(value, str):
            escaped = (
                value
                .replace("\\", "\\\\")
                .replace('"', '\\"')
            )

            return f'"{escaped}"'

        # ----------------------------------------------------
        # NULL
        # ----------------------------------------------------

        elif value is None:
            return "null"

        # ----------------------------------------------------------
        # OTHERS
        # ----------------------------------------------------------

        from datagen.function.commands._data.entitydata import EntityData, BlockEntityData
        from datagen.function.function import Function
        if isinstance(value, Function):
            return f'"{value.id}"'

        if isinstance(value, EntityData):
            return f'"{value.get_target()}"'

        if isinstance(value, BlockEntityData):
            return f'"{value.get_pos()}"'
        
        if isinstance(value, Range):
            return dumps(value.to_dict())

        if isinstance(value, bytes):
            return f'"{value.decode("utf-8")}"'

        if isinstance(value, bytearray):
            return f'"{value.decode("utf-8")}"'
        
        if isinstance(value, set):
            return (
                "["
                + ",".join(
                    SNBTSerializer._serialize_value(v)
                    for v in value
                )
                + "]"
            )

        if isinstance(value, tuple):
            return (
                "["
                + ",".join(
                    SNBTSerializer._serialize_value(v)
                    for v in value
                )
                + "]"
            )
        
        from datagen.function.commands._data.datastorage import DataStorage
        if isinstance(value, DataStorage):
            return f'"{value._id_str()}"'
        
        if isinstance(value, FunctionMacroArgument):
            return f'{value.__str__()}'
        
        if isinstance(value, Color):
            return f'{value.to_hex()}'

        if isinstance(value, Holder):
            return SNBTSerializer._serialize_value(value.get())

        raise TypeError(
            f"Unsupported type: {type(value)}"
        )

    @staticmethod
    def _escape_key(key: str) -> str:
        if re.fullmatch(r"[A-Za-z0-9._+-]+", key):
            return key

        escaped = (
            key
            .replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        return f'"{escaped}"'

    # ========================================================
    # DESERIALIZE
    # ========================================================

    @staticmethod
    def deserialize(snbt: str) -> dict[str, Any]:
        parser = _SNBTParser(snbt)

        value = parser.parse()

        if not isinstance(value, dict):
            raise ValueError(
                "Root SNBT value must be a compound"
            )

        return value


# ============================================================
# PARSER
# ============================================================

class _SNBTParser:

    def __init__(self, text: str):
        self.text = text
        self.i = 0

    # ========================================================
    # MAIN
    # ========================================================

    def parse(self) -> Any:
        self._skip_ws()

        value = self._parse_value()

        self._skip_ws()

        if self.i != len(self.text):
            raise ValueError(
                f"Unexpected trailing data at {self.i}"
            )

        return value

    # ========================================================
    # VALUES
    # ========================================================

    def _parse_value(self) -> Any:
        self._skip_ws()

        c = self._peek()

        if c == "{":
            return self._parse_compound()

        if c == "[":
            return self._parse_list_or_array()

        if c in ('"', "'"):
            return self._parse_string()

        return self._parse_literal()

    # ========================================================
    # COMPOUND
    # ========================================================

    def _parse_compound(self) -> dict[str, Any]:

        obj = {}

        self._expect("{")

        self._skip_ws()

        while self._peek() != "}":

            key = self._parse_key()

            self._skip_ws()

            self._expect(":")

            self._skip_ws()

            value = self._parse_value()

            obj[key] = value

            self._skip_ws()

            if self._peek() == ",":
                self.i += 1
                self._skip_ws()
            else:
                break

        self._expect("}")

        return obj

    # ========================================================
    # LIST / ARRAY
    # ========================================================

    def _parse_list_or_array(self):

        # -----------------------------------------------
        # Detect typed arrays
        # -----------------------------------------------

        if (
            self.i + 2 < len(self.text)
            and self.text[self.i] == "["
            and self.text[self.i + 2] == ";"
        ):

            array_type = self.text[self.i + 1]

            if array_type in ("B", "I", "L"):
                return self._parse_typed_array(array_type)

        return self._parse_list()

    # ========================================================
    # TYPED ARRAY
    # ========================================================

    def _parse_typed_array(self, array_type: str):

        self._expect("[")
        self.i += 1  # B/I/L
        self._expect(";")

        self._skip_ws()

        values = []

        while self._peek() != "]":

            token = self._parse_literal()

            values.append(token)

            self._skip_ws()

            if self._peek() == ",":
                self.i += 1
                self._skip_ws()
            else:
                break

        self._expect("]")

        if array_type == "B":
            return ByteArray(values)

        if array_type == "I":
            return IntArray(values)

        return LongArray(values)

    # ========================================================
    # NORMAL LIST
    # ========================================================

    def _parse_list(self):

        arr = []

        self._expect("[")

        self._skip_ws()

        while self._peek() != "]":

            arr.append(self._parse_value())

            self._skip_ws()

            if self._peek() == ",":
                self.i += 1
                self._skip_ws()
            else:
                break

        self._expect("]")

        return arr

    # ========================================================
    # STRING
    # ========================================================

    def _parse_string(self) -> str:

        quote = self._peek()

        self.i += 1

        result = []

        while self.i < len(self.text):

            c = self.text[self.i]

            if c == "\\":

                self.i += 1

                if self.i >= len(self.text):
                    raise ValueError("Invalid escape")

                result.append(self.text[self.i])

            elif c == quote:

                self.i += 1

                return "".join(result)

            else:
                result.append(c)

            self.i += 1

        raise ValueError("Unterminated string")

    # ========================================================
    # LITERAL
    # ========================================================

    def _parse_literal(self):

        start = self.i

        while (
            self.i < len(self.text)
            and self.text[self.i] not in ",}]"
        ):
            self.i += 1

        token = self.text[start:self.i].strip()

        # ----------------------------------------------------
        # BOOL
        # ----------------------------------------------------

        if token == "true":
            return True

        if token == "false":
            return False

        # ----------------------------------------------------
        # NULL
        # ----------------------------------------------------

        if token == "null":
            return None

        # ----------------------------------------------------
        # BYTE
        # ----------------------------------------------------

        if re.fullmatch(r"-?\d+b", token, re.IGNORECASE):
            return int(token[:-1])

        # ----------------------------------------------------
        # SHORT
        # ----------------------------------------------------

        if re.fullmatch(r"-?\d+s", token, re.IGNORECASE):
            return int(token[:-1])

        # ----------------------------------------------------
        # LONG
        # ----------------------------------------------------

        if re.fullmatch(r"-?\d+l", token, re.IGNORECASE):
            return int(token[:-1])

        # ----------------------------------------------------
        # FLOAT
        # ----------------------------------------------------

        if re.fullmatch(
            r"-?\d+(\.\d+)?f",
            token,
            re.IGNORECASE
        ):
            return float(token[:-1])

        # ----------------------------------------------------
        # DOUBLE
        # ----------------------------------------------------

        if re.fullmatch(
            r"-?\d+(\.\d+)?d",
            token,
            re.IGNORECASE
        ):
            return float(token[:-1])

        # ----------------------------------------------------
        # INT
        # ----------------------------------------------------

        if re.fullmatch(r"-?\d+", token):
            return int(token)

        # ----------------------------------------------------
        # BARE STRING
        # ----------------------------------------------------

        return token

    # ========================================================
    # KEYS
    # ========================================================

    def _parse_key(self):

        self._skip_ws()

        if self._peek() in ('"', "'"):
            return self._parse_string()

        start = self.i

        while (
            self.i < len(self.text)
            and self.text[self.i] != ":"
        ):
            self.i += 1

        return self.text[start:self.i].strip()

    # ========================================================
    # HELPERS
    # ========================================================

    def _peek(self):

        if self.i >= len(self.text):
            return "\0"

        return self.text[self.i]

    def _expect(self, char: str):

        if self._peek() != char:
            raise ValueError(
                f"Expected '{char}' at {self.i}"
            )

        self.i += 1

    def _skip_ws(self):

        while (
            self.i < len(self.text)
            and self.text[self.i].isspace()
        ):
            self.i += 1
