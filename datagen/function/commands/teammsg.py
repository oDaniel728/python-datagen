from datagen.function.commands.command import Command

class TeamMSG(Command):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def to_string(self) -> str:
        return f"teammsg {self.text}"