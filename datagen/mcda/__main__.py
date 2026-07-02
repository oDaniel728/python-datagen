import argparse
import sys
from pathlib import Path

from datagen.mcda import MCDACompiler


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m datagen.mcda",
        description="MCDA (Minecraft Datapack Assembly) compiler",
    )
    parser.add_argument("source", help="Path to .mcda source file")
    parser.add_argument("-o", "--output", default="datapacks/mcda",
                        help="Output directory (default: datapacks/mcda)")
    parser.add_argument("-w", "--watch", action="store_true",
                        help="Watch mode: rebuild on file changes")

    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        sys.exit(f"Error: source file not found: {source}")

    MCDACompiler().compile_file(source, args.output)
    print(f"Built datapack at {args.output}/")

    if args.watch:
        try:
            from datagen.utils.filewatcher import FileWatcher
            watcher = FileWatcher(str(source))
            watcher.watch(lambda p: MCDACompiler().compile_file(p, args.output))
        except ImportError:
            sys.exit("Watch mode requires datagen.utils.filewatcher")


if __name__ == "__main__":
    main()
