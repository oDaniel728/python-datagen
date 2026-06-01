from typing import Literal

from datagen.types.protocols.todict import ToDict


class BlockSettings():
    class LOGS(ToDict):
        TAxis = Literal["x", "y", "z"]
        def __init__(self, axis: TAxis):
            self.axis = axis

        def to_dict(self) -> dict:
            return {"axis": self.axis}