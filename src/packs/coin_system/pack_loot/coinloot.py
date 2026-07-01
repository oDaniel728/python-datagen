from datagen.loot_table.loot_table import LootTableBuilder
from datagen.types.util.min import Range
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.item import Item
from datagen.utils.repr.levelbasedvalue import LevelBasedValue, LevelBasedValues
from packs.coin_system.data.csys.enchantment.bundles import BUNDLES
from packs.coin_system.data.csys.enchantment.coins import COINS
from packs.coin_system.data.csys.enchantment.emeralds import EMERALDS
from packs.coin_system.data.csys.enchantment.items import ITEMS


class CoinLoot(LootTableBuilder):
    
    def __init__(self, id: Identifier) -> None:
        super().__init__(id)
        self.context_type("minecraft:entity")

    def add_coin(
        self,
        coin: Item,
        amount: Range = Range(1, 1),
        weight: int = 1,
    ):
        (
            self.pool(amount.to_dict())
                .entry(name=coin)
                    .weight(weight)
                .then()
            .end_pool()
        )
        return self

    def add_coin_with_bonus(
        self,
        coin: Item,
        base_amount: Range,
        bonus_amount: Range,
        weight: int = 1,
        unenchanted_chance: float = 0.0,
        enchanted_chance: LevelBasedValue | list[float] = LevelBasedValues.linear(0.05, 0.095),
    ):
        (
            self.pool(base_amount.to_dict())
                .entry(name=coin)
                    .weight(weight)
                .then()
            .end_pool()
        )
        (
            self.pool(bonus_amount.to_dict())
                .entry(name=coin)
                    .weight(weight)
                .then()
                .condition(lambda b: b.random_chance_with_enchanted_bonus(
                    COINS.id, unenchanted_chance, enchanted_chance
                ))
            .end_pool()
        )
        return self
    
    def add_emerald_coin_with_bonus(
        self,
        coin: Item,
        base_amount: Range,
        bonus_amount: Range,
        weight: int = 1,
        unenchanted_chance: float = 0.0,
        enchanted_chance: LevelBasedValue | list[float] = LevelBasedValues.linear(0.05, 0.095),
    ):
        (
            self.pool(base_amount.to_dict())
                .entry(name=coin)
                    .weight(weight)
                .then()
            .end_pool()
        )
        (
            self.pool(bonus_amount.to_dict())
                .entry(name=coin)
                    .weight(weight)
                .then()
                .condition(lambda b: b.random_chance_with_enchanted_bonus(
                    EMERALDS.id, unenchanted_chance, enchanted_chance
                ))
            .end_pool()
        )
        return self
    
    def add_bundle(
        self,
        bundle: Item,
        amount: Range = Range(1, 1),
        weight: int = 1,
        unenchanted_chance: float = 0.0,
        enchanted_chance: LevelBasedValue | list[float] = LevelBasedValues.linear(0.05, 0.05),
    ):
        (
            self.pool(amount.to_dict())
                .entry(name=bundle)
                    .weight(weight)
                .then()
                    .condition(lambda b: b.random_chance_with_enchanted_bonus(
                        BUNDLES.id, unenchanted_chance, enchanted_chance
                    ))
            .end_pool()
        )
        return self

    def add_item(
        self,
        item: Item,
        amount: Range = Range(1, 1),
        weight: int = 1,
        unenchanted_chance: float = 0.0,
        enchanted_chance: LevelBasedValue | list[float] = LevelBasedValues.linear(0.05, 0.095),
    ):
        (
            self.pool(amount.to_dict())
                .entry(name=item)
                    .weight(weight)
                .then()
                    .condition(lambda b: b.random_chance_with_enchanted_bonus(
                        ITEMS.id, unenchanted_chance, enchanted_chance
                    ))
            .end_pool()
        )
        return self

    def __invert__(self):
        return self.seal()
