from typing import Self

from datagen.utils.repr.itemstack import ItemStack
from datagen.types.util.reprs import *


class VillagerTradeOffer():
    def __init__(self):
        self.__buy: ItemStack | None = None
        self.__buy_b: ItemStack | None = None
        self.__sell: ItemStack | None = None
        self.__max_uses: int = 12
        self.__uses: int = 0
        self.__reward_exp: boolean = 1
        self.__price_multiplier: float = 0.0
        self.__xp: int = 1
        self.__special_price: int = 0
        self.__demand: int = 0

    def with_buy(self, item: ItemStack) -> Self:
        self.__buy = item
        return self

    def with_buy_b(self, item: ItemStack) -> Self:
        self.__buy_b = item
        return self

    def with_sell(self, item: ItemStack) -> Self:
        self.__sell = item
        return self

    def with_max_uses(self, value: int) -> Self:
        self.__max_uses = value
        return self

    def with_uses(self, value: int) -> Self:
        self.__uses = value
        return self

    def with_reward_exp(self, value: boolean) -> Self:
        self.__reward_exp = int(value)
        return self

    def with_price_multiplier(self, value: float) -> Self:
        self.__price_multiplier = value
        return self

    def with_xp(self, value: int) -> Self:
        self.__xp = value
        return self

    def with_special_price(self, value: int) -> Self:
        self.__special_price = value
        return self

    def with_demand(self, value: int) -> Self:
        self.__demand = value
        return self

    def to_dict(self) -> dict:
        result: dict = {
            "buy": self.__buy.to_dict() if self.__buy else None,
            "sell": self.__sell.to_dict() if self.__sell else None,
            "maxUses": self.__max_uses,
            "uses": self.__uses,
            "rewardExp": self.__reward_exp,
            "priceMultiplier": self.__price_multiplier,
            "xp": self.__xp,
            "specialPrice": self.__special_price,
            "demand": self.__demand,
        }
        if self.__buy_b is not None:
            result["buyB"] = self.__buy_b.to_dict()
        return result
