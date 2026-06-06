from datagen.datapack.datapack import DataPack
from datagen.function.anonymousfunction import AnonymousFunction
from datagen.function.commands.command import Command
from datagen.function.commands.customcommand import CustomCommand
from datagen.function.commands.runfunction import RunFunction
from datagen.function.function import Function
from datagen.utils.minecraft.targetselector import TargetSelector
from datagen.utils.minecraft.text import Text


class Title():
    @staticmethod
    def title(target: TargetSelector, title: Text.BaseText):
        return CustomCommand(f"title {target} title {title}")
    
    @staticmethod
    def subtitle(target: TargetSelector, subtitle: Text.BaseText):
        return CustomCommand(f"title {target} subtitle {subtitle}")
    
    @staticmethod
    def actionbar(target: TargetSelector, actionbar: Text.BaseText):
        return CustomCommand(f"title {target} actionbar {actionbar}")
    
    @staticmethod
    def times(target: TargetSelector, fadeIn: int, stay: int, fadeOut: int):
        return CustomCommand(f"title {target} times {fadeIn} {stay} {fadeOut}")
    
    @staticmethod
    def clear(target: TargetSelector):
        return CustomCommand(f"title {target} clear")
    
    @staticmethod
    def reset(target: TargetSelector):
        return CustomCommand(f"title {target} reset")

    def __init__(self):
        self.commands = list[Command]()

    def set_title(self, target: TargetSelector, title: Text.BaseText):
        self.commands.append(self.title(target, title))
        return self
    
    def set_subtitle(self, target: TargetSelector, subtitle: Text.BaseText):
        self.commands.append(self.subtitle(target, subtitle))
        return self
    
    def set_actionbar(self, target: TargetSelector, actionbar: Text.BaseText):
        self.commands.append(self.actionbar(target, actionbar))
        return self
    
    def set_times(self, target: TargetSelector, fadeIn: int, stay: int, fadeOut: int):
        self.commands.append(self.times(target, fadeIn, stay, fadeOut))
        return self
    
    def set_clear(self, target: TargetSelector):
        self.commands.append(self.clear(target))
        return self
    
    def set_reset(self, target: TargetSelector):
        self.commands.append(self.reset(target))
        return self
    
    def build(self) -> Function:
        return AnonymousFunction(DataPack.get_current_datapack()).add_commands(*self.commands)