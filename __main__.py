from pathlib import Path
from sys import argv
from datagen.utils.filewatcher import FileWatcher

import sys
sys.path.append((Path(__file__).parent.absolute().resolve() / "src").__str__())

import src.main


if __name__ == "__main__":
    try:
        if "--watch" in argv or "-w" in argv:
            def _(p):
                import importlib
                importlib.reload(src.main)
                src.main.main()

            for f in Path(src.main.__file__).parent.iterdir():
                FileWatcher(f).watch(_)
        else:
            src.main.main()
    except KeyboardInterrupt:
        print("Exiting...")