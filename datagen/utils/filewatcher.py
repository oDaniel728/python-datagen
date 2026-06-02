from pathlib import Path
from time import sleep
from typing import Callable


class FileWatcher:
    def __init__(self, file: str | Path):
        self.path = Path(file)
        self._last_mtime = self.path.stat().st_mtime

    def watch(self, callback: Callable[[Path], None], interval: float = 1.0):
        while True:
            mtime = self.path.stat().st_mtime

            if mtime != self._last_mtime:
                self._last_mtime = mtime
                callback(self.path)

            sleep(interval)