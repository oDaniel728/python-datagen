from datagen.main.datagensettings import DataGenSettings


class DataGen():
    def __init__(self, settings: DataGenSettings) -> None:
        self.settings = settings