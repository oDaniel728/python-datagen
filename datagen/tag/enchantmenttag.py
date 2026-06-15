from typing import Iterable

from datagen.tag.tag import Tag
from datagen.utils.minecraft.identifier import Identifier
from datagen.utils.repr.enchantment import Enchantment


class EnchantmentTag(Tag[Enchantment]):
    def __init__(self, id: Identifier, values: Iterable[Enchantment] = [], replace: bool = False):
        super().__init__(id, values, replace)
        self.type = Enchantment
