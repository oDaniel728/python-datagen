from datagen.utils.repr.block import Block


class ToolRule:
    def __init__(self) -> None:
        self._data = {}
        self.damage_per_block: int | None = None
        self.default_mining_speed: float | None = None
        self.rules: list[dict] = []

    def set_damage_per_block(self, damage: int):
        self.damage_per_block = damage
        return self
    
    def set_default_mining_speed(self, speed: float):
        self.default_mining_speed = speed
        return self

    def add_rule(self, blocks: list[Block], correct_for_drops: bool = True, speed: float = 1):
        self.rules.append({
            "blocks": [str(block.id) for block in blocks],
            "correct_for_drops": correct_for_drops,
            "speed": speed
        })
        return self
    
    def to_dict(self) -> dict:
        data = {}
        if self.damage_per_block is not None:
            data["damage_per_block"] = self.damage_per_block
        if self.default_mining_speed is not None:
            data["default_mining_speed"] = self.default_mining_speed
        if self.rules:
            data["rules"] = self.rules
        return data