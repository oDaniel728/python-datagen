
from datagen.function.commands.command import Command
from datagen.utils.minecraft.collections.blocks import Blocks
from datagen.utils.minecraft.relativeblockposition import RelativeBlockPosition
from datagen.utils.repr.block import Block
from datagen.utils.repr.blockschematic import BlockSchematic
from datagenpp.extras.item.chaincommandblock import ChainCommandBlock
from datagenpp.extras.item.settings.commandblocksettings import CommandBlockSettings


class CommandBlock(Block[CommandBlockSettings]):
    def __init__(self, settings: CommandBlockSettings) -> None:
        super().__init__(Blocks.COMMAND_BLOCK.id)
        self.nbt = settings

    @staticmethod
    def create_chain(*commands: Command, direction: Block._TDirection = "up") -> BlockSchematic:
        _raws = list[str]()
        _raws.extend(list[str](map(lambda c: c.to_string(), commands)))
        schem = BlockSchematic()

        pos = RelativeBlockPosition(0, 0, 0)
        def move_front():
            nonlocal pos
            match direction:
                case "down": pos.set_y(pos.get_y_as(int) - 1)
                case "up": pos.set_y(pos.get_y_as(int) + 1)
                case "north": pos.set_z(pos.get_z_as(int) - 1)
                case "south": pos.set_z(pos.get_z_as(int) + 1)
                case "west": pos.set_x(pos.get_x_as(int) - 1)
                case "east": pos.set_x(pos.get_x_as(int) + 1)

        for i, raw in enumerate(_raws):
            _is_first = i == 0

            print(pos)
            if _is_first:
                schem += CommandBlock(
                    CommandBlockSettings(raw, direction, False, False)
                ).at(RelativeBlockPosition(pos.x, pos.y, pos.z))
            else:
                schem += ChainCommandBlock(
                    CommandBlockSettings(raw, direction, False, True)
                ).at(RelativeBlockPosition(pos.x, pos.y, pos.z))
            move_front()

        return schem