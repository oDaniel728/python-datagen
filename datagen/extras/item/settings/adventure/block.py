from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item
from datagen.extras.item.settings.adventure.tool import AdventureToolSettings


class AdventureBlockSettings(AdventureToolSettings):
    def __init__(
        self, 
        can_place_on: list[Block] = [],
        can_break: list[Block] = [],
        show_in_tooltip: bool = True,
    ) -> None:
        super().__init__(can_break, show_in_tooltip)
        self.can_place_on = can_place_on
    def get_components(self) -> dict:
        return super().get_components() | {
            "can_place_on": {
                "predicates": [
                    {
                        "blocks": [block.id],
                        "nbt": block.settings.get_block_entity_data(),
                        "state": block.settings.get_block_state(),
                    }
                    for block in self.can_place_on
                ],
                "show_in_tooltip": self.show_in_tooltip
            }
        }