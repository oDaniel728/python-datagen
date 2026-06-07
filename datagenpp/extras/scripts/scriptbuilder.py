from datagen.datapack.namespace import Namespace
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands._data.datastorage import DataStorage
from datagen.function.commands._return import Return
from datagen.function.commands.command import Command
from datagen.function.commands.execute import Execute
from datagen.function.commands.runfunction import RunFunction
from datagen.function.commands.scoreboard import Scoreboard
from datagen.function.function import Function
from datagen.predicate.predicate import Predicate
from datagen.types.util.counter import Counter
from datagen.types.util.min import Range
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text
from datagen.utils.repr.block import Block
from datagen.utils.repr.entitytype import EntityType
from datagen.utils.repr.item import Item
from datagen.utils.scoreboard.criterion import ObjectiveCriterion
from datagenpp.extras.scripts.script import Script

_tmp = Namespace.temp
_counter = Counter()
class ScriptBuilder:
    @staticmethod
    def on_use_of_item(item: Item, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_use_of_item_load_{i}")
        tick = Function(_tmp / f"__on_use_of_item_tick_{i}")

        obj = Scoreboard.objective(f"__use_of_item_{item.id.get_path()}", Text.literal(f"use of item {item.id}"), ObjectiveCriterion.used(item))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)


        with Function(_tmp / f"__on_use_of_item_lambda_{i}") as lambda_func:
            args = DataStorage(_tmp / f"__use_of_item_args_{i}")
            ~ args.set_from_entity("item", TargetSelector.SELF, "SelectedItem")
            ~ args.set_from_entity("slot", TargetSelector.SELF, "SelectedItemSlot")
            ~ args.set_from_entity("self", TargetSelector.SELF)
            ~ me.set(0)
            ~ Return.run(function.run(args))

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run())
        )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_killed_by_entity(entity: EntityType, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_killed_by_entity_load_{i}")
        tick = Function(_tmp / f"__on_killed_by_entity_tick_{i}")

        obj = Scoreboard.objective(f"__killed_by_entity_{entity.id.get_path()}", Text.literal(f"killed by entity {entity.id}"), ObjectiveCriterion.killed_by(entity))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_killed_by_entity_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"entity": f"{entity.id}"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_killed_entity(entity: EntityType, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_killed_entity_load_{i}")
        tick = Function(_tmp / f"__on_killed_entity_tick_{i}")

        obj = Scoreboard.objective(f"__killed_entity_{entity.id.get_path()}", Text.literal(f"killed entity {entity.id}"), ObjectiveCriterion.killed(entity))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_killed_entity_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"entity": f"{entity.id}"}))
        )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
    
    @staticmethod
    def on_item_drop(item: Item, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_item_drop_load_{i}")
        tick = Function(_tmp / f"__on_item_drop_tick_{i}")

        obj = Scoreboard.objective(f"__dropped_{item.id.get_path()}", Text.literal(f"dropped {item.id}"), ObjectiveCriterion.dropped(item))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        args = (
            DataStorage(_tmp / f"__on_item_drop_args_{i}")
        )

        with Function(_tmp / f"__on_item_drop_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"item": f"{item.id}", "drop": f"@e[type=item,nbt={{Item:{{id:\"minecraft:{item.id}\"}}}}]"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_item_pickup(item: Item, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_item_pickup_load_{i}")
        tick = Function(_tmp / f"__on_item_pickup_tick_{i}")

        obj = Scoreboard.objective(f"__picked_up_{item.id.get_path()}", Text.literal(f"picked up {item.id}"), ObjectiveCriterion.picked_up(item))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_item_pickup_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"item": f"{item.id}"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_block_mined(block: Block, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_block_mined_load_{i}")
        tick = Function(_tmp / f"__on_block_mined_tick_{i}")

        obj = Scoreboard.objective(f"__mined_{block.id.get_path()}", Text.literal(f"mined {block.id}"), ObjectiveCriterion.mined(block))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_block_mined_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"block": f"{block.id}"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_block_placed(block: Block, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_block_placed_load_{i}")
        tick = Function(_tmp / f"__on_block_placed_tick_{i}")

        obj = Scoreboard.objective(f"__placed_{block.id.get_path()}", Text.literal(f"placed {block.id}"), ObjectiveCriterion.used(block))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_block_placed_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"block": f"{block.id}"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_item_craft(item: Item, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_item_craft_load_{i}")
        tick = Function(_tmp / f"__on_item_craft_tick_{i}")

        obj = Scoreboard.objective(f"__crafted_{item.id.get_path()}", Text.literal(f"crafted {item.id}"), ObjectiveCriterion.crafted(item))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_item_craft_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func.run({"item": f"{item.id}"}))
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _

    @staticmethod
    def on_item_broken(item: Item, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_item_broken_load_{i}")
        tick = Function(_tmp / f"__on_item_broken_tick_{i}")

        obj = Scoreboard.objective(f"__broken_{item.id.get_path()}", Text.literal(f"broken {item.id}"), ObjectiveCriterion.broken(item))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_item_broken_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_jump(function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_jump_load_{i}")
        tick = Function(_tmp / f"__on_jump_tick_{i}")

        obj = Scoreboard.objective(f"__jump_{i}", Text.literal(f"jump"), ObjectiveCriterion.custom("minecraft.jump"))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_jump_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(1))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_walk(cm: int, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_walk_load_{i}")
        tick = Function(_tmp / f"__on_walk_tick_{i}")

        obj = Scoreboard.objective(f"__walk_cm_{i}", Text.literal(f"walked cm"), ObjectiveCriterion.custom("minecraft.walk_one_cm"))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_walk_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(cm))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_crouch(cm: int, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_crouch_load_{i}")
        tick = Function(_tmp / f"__on_crouch_tick_{i}")

        obj = Scoreboard.objective(f"__crouch_cm_{i}", Text.literal(f"crouched cm"), ObjectiveCriterion.custom("minecraft.crouch_one_cm"))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_crouch_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(cm))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_scoreboard_criteria_value_met(criterion: ObjectiveCriterion, value: Range, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_scoreboard_criteria_value_met_load_{i}")
        tick = Function(_tmp / f"__on_scoreboard_criteria_value_met_tick_{i}")

        obj = Scoreboard.objective(f"__criteria_{i}", Text.literal(f"criteria"), criterion)
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_scoreboard_criteria_value_met_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", value)
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_each_ticks_for_players(ticks: int, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_each_ticks_load_{i}")
        tick = Function(_tmp / f"__on_each_ticks_tick_{i}")

        obj = Scoreboard.objective(f"__ticks_{i}", Text.literal(f"ticks"), ObjectiveCriterion.custom("minecraft.tick"))
        all_players = obj.player(TargetSelector.ALL_PLAYERS)
        me = obj.player(TargetSelector.SELF)

        with Function(_tmp / f"__on_each_ticks_lambda_{i}") as lambda_func:
            ~ me.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(all_players.set(0))

        tick.add_command(all_players.add(1))
        tick.add_command(
            Execute()
            .AS(TargetSelector.ALL_PLAYERS)
            .AT(TargetSelector.SELF)
            .IF(
                lambda b: b.score(me, "matches", Range.min(ticks))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _
        
    @staticmethod
    def on_each_ticks_server(ticks: int, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_each_ticks_server_load_{i}")
        tick = Function(_tmp / f"__on_each_ticks_server_tick_{i}")

        obj = Scoreboard.objective(f"__server_ticks_{i}", Text.literal(f"server ticks"), ObjectiveCriterion.custom("minecraft.tick"))
        value = obj.player("value")

        with Function(_tmp / f"__on_each_ticks_server_lambda_{i}") as lambda_func:
            ~ value.set(0)
            ~ Return.function(function)

        load.add_command(obj.add())
        load.add_command(value.set(0))

        tick.add_command(value.add(1))
        tick.add_command(
            Execute()
            .IF(
                lambda b: b.score(value, "matches", Range.min(ticks))
            )
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _

    @staticmethod
    def on_predicate(predicate: Predicate, function: Function) -> Script:
        i = _counter.get()
        load = Function(_tmp / f"__on_predicate_load_{i}")
        tick = Function(_tmp / f"__on_predicate_tick_{i}")

        with Function(_tmp / f"__on_predicate_lambda_{i}") as lambda_func:
            ~ Return.function(function)

        tick.add_command(
            Execute()
            .IF(lambda b: b.predicate(predicate))
            .RUN(lambda_func)
         )

        with Script() as _:
            _.on_load(load)
            _.on_tick(tick)
            return _

