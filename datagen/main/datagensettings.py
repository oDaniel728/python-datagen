from dataclasses import dataclass


@dataclass
class DataGenSettings():
    def __init__(self,
        pack_format: int,
        namespace: str,
        description: str = "",
    ) -> None:
        self.pack_format = pack_format
        self.namespace = namespace