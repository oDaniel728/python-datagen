from sys import argv

from datagen.utils.filewatcher import FileWatcher
import src.main

if __name__ == "__main__":
    try:
        src.main.main()
        if "--watch" in argv or "-w" in argv:
            FileWatcher(src.main.__file__).watch(lambda _: src.main.main())
    except KeyboardInterrupt:
        print("Exiting...")