from datagen.function.commands.customcommand import CustomCommand


def version(v: str) -> CustomCommand:
    return CustomCommand("say Version: " + v)