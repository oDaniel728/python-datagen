from datagen.types.protocols.todict import ToDict
from datagen.utils.repr.levelbasedvalue import LevelBasedValue, LevelBasedValue, as_level


class ValueEffect(ToDict):
    @staticmethod
    def set_(value: float | LevelBasedValue) -> "ToDict":
        return ValueEffect._Set(value)

    @staticmethod
    def add(value: float | LevelBasedValue) -> "ToDict":
        return ValueEffect._Add(value)

    @staticmethod
    def multiply(factor: float | LevelBasedValue) -> "ToDict":
        return ValueEffect._Multiply(factor)

    @staticmethod
    def remove_binomial(chance: float | LevelBasedValue) -> "ToDict":
        return ValueEffect._RemoveBinomial(chance)

    @staticmethod
    def all_of(*effects: ToDict) -> "ToDict":
        return ValueEffect._AllOf(list(effects))

    class _Set(ToDict):
        def __init__(self, value: float | LevelBasedValue):
            self.value = value

        def to_dict(self) -> dict:
            return {"type": "minecraft:set", "value": as_level(self.value)}

    class _Add(ToDict):
        def __init__(self, value: float | LevelBasedValue):
            self.value = value

        def to_dict(self) -> dict:
            return {"type": "minecraft:add", "value": as_level(self.value)}

    class _Multiply(ToDict):
        def __init__(self, factor: float | LevelBasedValue):
            self.factor = factor

        def to_dict(self) -> dict:
            return {"type": "minecraft:multiply", "factor": as_level(self.factor)}

    class _RemoveBinomial(ToDict):
        def __init__(self, chance: float | LevelBasedValue):
            self.chance = chance

        def to_dict(self) -> dict:
            return {"type": "minecraft:remove_binomial", "chance": as_level(self.chance)}

    class _AllOf(ToDict):
        def __init__(self, effects: list[ToDict]):
            self.effects = effects

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:all_of",
                "effects": [e.to_dict() if hasattr(e, "to_dict") else e for e in self.effects]
            }


class EntityEffect(ToDict):
    @staticmethod
    def all_of(*effects: ToDict) -> "ToDict":
        return EntityEffect._AllOf(list(effects))

    @staticmethod
    def apply_mob_effect(
        to_apply: list[str],
        min_duration: float | LevelBasedValue,
        max_duration: float | LevelBasedValue,
        min_amplifier: float | LevelBasedValue,
        max_amplifier: float | LevelBasedValue
    ) -> "ToDict":
        return EntityEffect._ApplyMobEffect(to_apply, min_duration, max_duration, min_amplifier, max_amplifier)

    @staticmethod
    def damage_entity(
        damage_type: str,
        min_damage: float | LevelBasedValue,
        max_damage: float | LevelBasedValue
    ) -> "ToDict":
        return EntityEffect._DamageEntity(damage_type, min_damage, max_damage)

    @staticmethod
    def change_item_damage(amount: float | LevelBasedValue) -> "ToDict":
        return EntityEffect._ChangeItemDamage(amount)

    @staticmethod
    def ignite(duration: float | LevelBasedValue) -> "ToDict":
        return EntityEffect._Ignite(duration)

    @staticmethod
    def explode(
        radius: float | LevelBasedValue,
        block_interaction: str = "none",
        create_fire: bool = False,
        damage_type: str | None = None,
        knockback_multiplier: float | LevelBasedValue | None = None,
        offset: list[float] | None = None,
        immune_blocks: list[str] | None = None,
        sound: str | None = None,
        small_particle: dict | None = None,
        large_particle: dict | None = None,
        attribute_to_user: bool = False
    ) -> "ToDict":
        return EntityEffect._Explode(
            radius, block_interaction, create_fire, damage_type,
            knockback_multiplier, offset, immune_blocks, sound,
            small_particle, large_particle, attribute_to_user
        )

    @staticmethod
    def play_sound(
        sound: str | list[str],
        volume: float = 1.0,
        pitch: float = 1.0
    ) -> "ToDict":
        return EntityEffect._PlaySound(sound, volume, pitch)

    @staticmethod
    def replace_block(
        block_state: dict,
        offset: list[int] | None = None,
        predicate: dict | None = None,
        trigger_game_event: str | None = None
    ) -> "ToDict":
        return EntityEffect._ReplaceBlock(block_state, offset, predicate, trigger_game_event)

    @staticmethod
    def replace_disk(
        block_state: dict,
        radius: float | LevelBasedValue,
        height: float | LevelBasedValue,
        offset: list[int] | None = None,
        predicate: dict | None = None,
        trigger_game_event: str | None = None
    ) -> "ToDict":
        return EntityEffect._ReplaceDisk(block_state, radius, height, offset, predicate, trigger_game_event)

    @staticmethod
    def run_function(function: str) -> "ToDict":
        return EntityEffect._RunFunction(function)

    @staticmethod
    def set_block_properties(
        properties: dict[str, str],
        offset: list[int] | None = None,
        trigger_game_event: str | None = None
    ) -> "ToDict":
        return EntityEffect._SetBlockProperties(properties, offset, trigger_game_event)

    @staticmethod
    def spawn_particles(
        particle: dict,
        horizontal_position: dict | None = None,
        vertical_position: dict | None = None,
        speed: float = 0,
        horizontal_velocity: dict | None = None,
        vertical_velocity: dict | None = None
    ) -> "ToDict":
        return EntityEffect._SpawnParticles(particle, horizontal_position, vertical_position, speed, horizontal_velocity, vertical_velocity)

    @staticmethod
    def summon_entity(entity: str | list[str], join_team: bool = False) -> "ToDict":
        return EntityEffect._SummonEntity(entity, join_team)

    class _AllOf(ToDict):
        def __init__(self, effects: list[ToDict]):
            self.effects = effects

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:all_of",
                "effects": [e.to_dict() if hasattr(e, "to_dict") else e for e in self.effects]
            }

    class _ApplyMobEffect(ToDict):
        def __init__(self, to_apply, min_duration, max_duration, min_amplifier, max_amplifier):
            self.to_apply = to_apply if isinstance(to_apply, list) else [to_apply]
            self.min_duration = min_duration
            self.max_duration = max_duration
            self.min_amplifier = min_amplifier
            self.max_amplifier = max_amplifier

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:apply_mob_effect",
                "to_apply": self.to_apply,
                "min_duration": as_level(self.min_duration),
                "max_duration": as_level(self.max_duration),
                "min_amplifier": as_level(self.min_amplifier),
                "max_amplifier": as_level(self.max_amplifier)
            }

    class _DamageEntity(ToDict):
        def __init__(self, damage_type, min_damage, max_damage):
            self.damage_type = damage_type
            self.min_damage = min_damage
            self.max_damage = max_damage

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:damage_entity",
                "damage_type": self.damage_type,
                "min_damage": as_level(self.min_damage),
                "max_damage": as_level(self.max_damage)
            }

    class _ChangeItemDamage(ToDict):
        def __init__(self, amount):
            self.amount = amount

        def to_dict(self) -> dict:
            return {"type": "minecraft:change_item_damage", "amount": as_level(self.amount)}

    class _Ignite(ToDict):
        def __init__(self, duration):
            self.duration = duration

        def to_dict(self) -> dict:
            return {"type": "minecraft:ignite", "duration": as_level(self.duration)}

    class _Explode(ToDict):
        def __init__(self, radius, block_interaction, create_fire, damage_type,
                     knockback_multiplier, offset, immune_blocks, sound,
                     small_particle, large_particle, attribute_to_user):
            self.radius = radius
            self.block_interaction = block_interaction
            self.create_fire = create_fire
            self.damage_type = damage_type
            self.knockback_multiplier = knockback_multiplier
            self.offset = offset
            self.immune_blocks = immune_blocks
            self.sound = sound
            self.small_particle = small_particle
            self.large_particle = large_particle
            self.attribute_to_user = attribute_to_user

        def to_dict(self) -> dict:
            d: dict = {"type": "minecraft:explode", "radius": as_level(self.radius)}
            if not self.attribute_to_user:
                d["attribute_to_user"] = False
            else:
                d["attribute_to_user"] = True
            d["block_interaction"] = self.block_interaction
            d["create_fire"] = self.create_fire
            if self.damage_type is not None:
                d["damage_type"] = self.damage_type
            if self.knockback_multiplier is not None:
                d["knockback_multiplier"] = as_level(self.knockback_multiplier)
            if self.offset is not None:
                d["offset"] = self.offset
            if self.immune_blocks is not None:
                d["immune_blocks"] = self.immune_blocks
            if self.sound is not None:
                d["sound"] = self.sound
            if self.small_particle is not None:
                d["small_particle"] = self.small_particle
            if self.large_particle is not None:
                d["large_particle"] = self.large_particle
            return d

    class _PlaySound(ToDict):
        def __init__(self, sound, volume, pitch):
            self.sound = sound
            self.volume = volume
            self.pitch = pitch

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:play_sound",
                "sound": self.sound,
                "volume": self.volume,
                "pitch": self.pitch
            }

    class _ReplaceBlock(ToDict):
        def __init__(self, block_state, offset, predicate, trigger_game_event):
            self.block_state = block_state
            self.offset = offset
            self.predicate = predicate
            self.trigger_game_event = trigger_game_event

        def to_dict(self) -> dict:
            d: dict = {"type": "minecraft:replace_block", "block_state": self.block_state}
            if self.offset is not None:
                d["offset"] = self.offset
            if self.predicate is not None:
                d["predicate"] = self.predicate
            if self.trigger_game_event is not None:
                d["trigger_game_event"] = self.trigger_game_event
            return d

    class _ReplaceDisk(ToDict):
        def __init__(self, block_state, radius, height, offset, predicate, trigger_game_event):
            self.block_state = block_state
            self.radius = radius
            self.height = height
            self.offset = offset
            self.predicate = predicate
            self.trigger_game_event = trigger_game_event

        def to_dict(self) -> dict:
            d: dict = {
                "type": "minecraft:replace_disk",
                "block_state": self.block_state,
                "radius": as_level(self.radius),
                "height": as_level(self.height)
            }
            if self.offset is not None:
                d["offset"] = self.offset
            if self.predicate is not None:
                d["predicate"] = self.predicate
            if self.trigger_game_event is not None:
                d["trigger_game_event"] = self.trigger_game_event
            return d

    class _RunFunction(ToDict):
        def __init__(self, function):
            self.function = function

        def to_dict(self) -> dict:
            return {"type": "minecraft:run_function", "function": self.function}

    class _SetBlockProperties(ToDict):
        def __init__(self, properties, offset, trigger_game_event):
            self.properties = properties
            self.offset = offset
            self.trigger_game_event = trigger_game_event

        def to_dict(self) -> dict:
            d: dict = {"type": "minecraft:set_block_properties", "properties": self.properties}
            if self.offset is not None:
                d["offset"] = self.offset
            if self.trigger_game_event is not None:
                d["trigger_game_event"] = self.trigger_game_event
            return d

    class _SpawnParticles(ToDict):
        def __init__(self, particle, horizontal_position, vertical_position, speed, horizontal_velocity, vertical_velocity):
            self.particle = particle
            self.horizontal_position = horizontal_position
            self.vertical_position = vertical_position
            self.speed = speed
            self.horizontal_velocity = horizontal_velocity
            self.vertical_velocity = vertical_velocity

        def to_dict(self) -> dict:
            d: dict = {"type": "minecraft:spawn_particles", "particle": self.particle}
            if self.horizontal_position is not None:
                d["horizontal_position"] = self.horizontal_position
            if self.vertical_position is not None:
                d["vertical_position"] = self.vertical_position
            if self.speed:
                d["speed"] = as_level(self.speed)
            if self.horizontal_velocity is not None:
                d["horizontal_velocity"] = self.horizontal_velocity
            if self.vertical_velocity is not None:
                d["vertical_velocity"] = self.vertical_velocity
            return d

    class _SummonEntity(ToDict):
        def __init__(self, entity, join_team):
            self.entity = entity if isinstance(entity, list) else [entity]
            self.join_team = join_team

        def to_dict(self) -> dict:
            return {
                "type": "minecraft:summon_entity",
                "entity": self.entity,
                "join_team": self.join_team
            }


class AttributeEffect(ToDict):
    def __init__(self, attribute: str, amount: float | LevelBasedValue, operation: str, id: str):
        self.attribute = attribute
        self.amount = amount
        self.operation = operation
        self.id = id

    def to_dict(self) -> dict:
        return {
            "attribute": self.attribute,
            "amount": as_level(self.amount),
            "operation": self.operation,
            "id": self.id
        }


class EffectComponent:
    @staticmethod
    def value_component(effect: ToDict, requirements: dict | None = None, enchanted: str | None = None) -> dict:
        d: dict = {"effect": effect.to_dict() if hasattr(effect, "to_dict") else effect}
        if requirements is not None:
            d["requirements"] = requirements
        if enchanted is not None:
            d["enchanted"] = enchanted
        return d

    @staticmethod
    def entity_component(effect: ToDict, enchanted: str, affected: str, requirements: dict | None = None) -> dict:
        d: dict = {
            "effect": effect.to_dict() if hasattr(effect, "to_dict") else effect,
            "enchanted": enchanted,
            "affected": affected
        }
        if requirements is not None:
            d["requirements"] = requirements
        return d
