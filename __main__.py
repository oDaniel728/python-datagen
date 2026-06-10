from pathlib import Path
from sys import argv
from datagen.utils.filewatcher import FileWatcher

import sys
sys.path.append((Path(__file__).parent.absolute().resolve() / "src").__str__())

import src.main


if __name__ == "__main__":
    try:
        src.main.main()
        if "--watch" in argv or "-w" in argv:
            @FileWatcher(src.main.__file__).watch
            def _(p):
                import importlib
                importlib.reload(src.main)
                src.main.main()
    except KeyboardInterrupt:
        print("Exiting...")