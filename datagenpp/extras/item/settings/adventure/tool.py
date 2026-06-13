from datagen.utils.repr.block import Block
from datagen.utils.repr.item import Item


class AdventureToolSettings(Item.Settings):
    def __init__(
        self,
        can_break: list[Block] = [],
        show_in_tooltip: bool = True,
    ) -> None:
        super().__init__()
        self.can_break = can_break
        self.show_in_tooltip = show_in_tooltip
    def get_components(self) -> dict:
        return {
            "can_break": {
                "predicates": [
                    {
                        "blocks": [~block.id],
                        "nbt": block.settings.get_block_entity_data(),
                        "state": block.settings.get_block_state(),
                    }
                    for block in self.can_break
                ],
                "show_in_tooltip": self.show_in_tooltip
            }
        }