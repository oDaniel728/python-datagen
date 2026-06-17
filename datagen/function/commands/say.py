from datagen.function.commands.command import Command


class Say(Command):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def to_string(self) -> str:
        msg = str(self.message)
        return self.auto_macro("say " + msg)