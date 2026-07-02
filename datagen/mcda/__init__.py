from pathlib import Path

from datagen.mcda.compiler import MCDACompiler


def compile_file(source_path: str, output_dir: str = "datapacks/mcda") -> None:
    MCDACompiler().compile_file(source_path, output_dir)


def compile_string(source: str, output_dir: str = "datapacks/mcda") -> None:
    MCDACompiler().compile_string(source, Path(output_dir))
