from typing import Any, NotRequired, Optional, TypedDict

from datagen.types.util.min import Range
from datagen.types.util.validpredicate import ValidPredicate
from datagen.utils.dictfilter import filter_dict
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.equipment_slot import EquipmentSlot
from datagen.utils.repr.itempredicate import ItemPredicate
from datagen.utils.repr.locationpredicate import LocationPredicate
from datagen.utils.repr.slot_range import SlotRange
from datagen.utils.repr.status_effect import StatusEffect
from datagen.utils.repr.typespecificpredicate import TypeSpecificPredicate

# FINISHED
class EntityPredicate(ValidPredicate):
    def __init__(self) -> None:
        self._data: dict = {}

    def with_type(self, entity_type: EntityType) -> "EntityPredicate":
        self._data["type"] = str(entity_type)
        return self

    def with_distance(
        self,
        absolute: int | Range | None = None,
        horizontal: int | Range | None = None,
        x: int | Range | None = None,
        y: int | Range | None = None,
        z: int | Range | None = None
    ) -> "EntityPredicate":
        def _auto_int_range(value: int | Range | None):
            if not isinstance(value, int) and value:
                return value.to_dict()
            return value
        self._data["distance"] = filter_dict({
            "absolute": absolute,
            "horizontal": horizontal,
            "x": _auto_int_range(x),
            "y": _auto_int_range(y),
            "z": _auto_int_range(z)
        })
        return self

    class _TRange(TypedDict):
        min: NotRequired[int]
        max: NotRequired[int]
    class _TEffect(TypedDict):
        amplifier: NotRequired[int | EntityPredicate._TRange | Range]
        duration: NotRequired[int | EntityPredicate._TRange | Range]
        ambient: NotRequired[bool]
        visible: NotRequired[bool]

    def with_effects(self, effects: dict[StatusEffect, _TEffect]) -> "EntityPredicate":
        effects_data = dict()
        for effect, data in effects.items():
            effect_data: dict[str, Any] = {}
            if "ambient" in data:
                effect_data["ambient"] = data["ambient"]
            if "visible" in data:
                effect_data["visible"] = data["visible"]

            if "amplifier" in data:
                amplifier = data["amplifier"]
                if isinstance(amplifier, (int, dict)):
                    effect_data["amplifier"] = amplifier
                else:
                    effect_data["amplifier"] = amplifier.to_dict()
            if "duration" in data:
                duration = data["duration"]
                if isinstance(duration, (int, dict)):
                    effect_data["duration"] = duration
                else:
                    effect_data["duration"] = duration.to_dict()

            effects_data[str(effect.id)] = effect_data
        self._data["effects"] = effects_data
        return self

    def with_location(self, location: LocationPredicate) -> "EntityPredicate":
        self._data["location"] = location.to_dict()
        return self

    def with_equipment(self, slot: EquipmentSlot, item: ItemPredicate) -> "EntityPredicate":
        equipment = self._data.setdefault("equipment", {})
        equipment[str(slot)] = item.to_dict()
        return self

    def with_nbt(self, nbt: str) -> "EntityPredicate":
        self._data["nbt"] = nbt
        return self
    
    def with_flags(self,
        is_baby: Optional[bool] = None,
        is_on_fire: Optional[bool] = None,
        is_sneaking: Optional[bool] = None,
        is_sprinting: Optional[bool] = None,
        is_swimming: Optional[bool] = None,
        in_on_ground: Optional[bool] = None,
        is_flying: Optional[bool] = None,
        is_fall_flying: Optional[bool] = None,
    ) -> "EntityPredicate":
        flags = self._data.setdefault("flags", {})
        if is_baby is not None: flags["is_baby"] = is_baby
        if is_on_fire is not None: flags["is_on_fire"] = is_on_fire
        if is_sneaking is not None: flags["is_sneaking"] = is_sneaking
        if is_sprinting is not None: flags["is_sprinting"] = is_sprinting
        if is_swimming is not None: flags["is_swimming"] = is_swimming
        if in_on_ground is not None: flags["in_on_ground"] = in_on_ground
        if is_flying is not None: flags["is_flying"] = is_flying
        if is_fall_flying is not None: flags["is_fall_flying"] = is_fall_flying
        return self
    
    def with_passenger(self, passenger: "EntityPredicate") -> "EntityPredicate":
        passengers: list = self._data.setdefault("passengers", [])
        passengers.append(passenger.to_dict())
        return self
    
    def with_slots(self, slots: "dict[SlotRange, ItemPredicate]") -> "EntityPredicate":
        slots_data = self._data.setdefault("slots", {})
        for slot_range, item_pred in slots.items():
            slots_data[str(slot_range)] = item_pred.to_dict()
        return self
    
    def with_stepping_on(self, location: "LocationPredicate") -> "EntityPredicate":
        self._data["stepping_on"] = location.to_dict()
        return self
    
    def with_movement_affected_by(self, location: "LocationPredicate") -> "EntityPredicate":
        self._data["movement_affected_by"] = location.to_dict()
        return self
    
    def with_team(self, team: str) -> "EntityPredicate":
        self._data["team"] = team
        return self
    
    def with_targeted_entity(self, entity: "EntityPredicate") -> "EntityPredicate":
        self._data["targeted_entity"] = entity.to_dict()
        return self
    
    def with_vehicle(self, vehicle: "EntityPredicate") -> "EntityPredicate":
        self._data["vehicle"] = vehicle.to_dict()
        return self
    
    def with_movement(self,
        x: int | Range | None = None,
        y: int | Range | None = None,
        z: int | Range | None = None,
        speed: int | Range | None = None,
        horizontal_speed: int | Range | None = None,
        vertical_speed: int | Range | None = None,
        fall_distance: int | Range | None = None
    ) -> "EntityPredicate":
        def _auto_int_range(value: int | Range | None):
            if not isinstance(value, int) and value:
                return value.to_dict()
            return value
        movement = self._data.setdefault("movement", {})
        if x is not None: movement["x"] = _auto_int_range(x)
        if y is not None: movement["y"] = _auto_int_range(y)
        if z is not None: movement["z"] = _auto_int_range(z)
        if speed is not None: movement["speed"] = _auto_int_range(speed)
        if horizontal_speed is not None: movement["horizontal_speed"] = _auto_int_range(horizontal_speed)
        if vertical_speed is not None: movement["vertical_speed"] = _auto_int_range(vertical_speed)
        if fall_distance is not None: movement["fall_distance"] = _auto_int_range(fall_distance)
        return self
    
    def with_periodic_tick(self, period: int) -> "EntityPredicate":
        self._data["periodic_tick"] = period
        return self

    def with_predicates(self, predicates: dict[str, Any]) -> "EntityPredicate":
        for key, value in predicates.items():
            self._data[key] = value
        return self
    
    def with_type_specific(self, data: TypeSpecificPredicate):
        self._data["type_specific"] = data.to_dict()
        return self

    def set(self, key: str, value) -> "EntityPredicate":
        self._data[key] = value
        return self

    def to_dict(self) -> dict:
        return self._data
