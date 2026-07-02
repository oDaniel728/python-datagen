
from typing import Iterable

from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.minecraft.text._base import BaseText
from datagen.utils.repr.enchantment_provider import EnchantmentProvider


def basic_enchantment(
    id: Identifier, 
    desc: BaseText, 
    max_level: int, 
    weight: int, 
    cost: tuple[int, int, int, int], 
    anvil_cost: int, 
    items: Iterable
) -> EnchantmentProvider:
    return EnchantmentProvider(id) \
        .with_description(desc) \
        .with_max_level(max_level) \
        .with_supported_items(*items) \
        .with_primary_items(*items) \
        .with_weight(weight) \
        .with_cost(*cost) \
        .with_anvil_cost(anvil_cost) \
        .with_slots("any")