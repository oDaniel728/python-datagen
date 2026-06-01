from pathlib import Path


class SimpleFile():
    def __init__(self, path: str | Path, content: str = "") -> None:
        self.path = Path(path)
        self.content = content

    def build(self, base: str | Path):
        fp = Path(base) / self.path
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(self.content)

    def write(self, content: str):
        self.content = content

    def rename(self, name: str):
        self.path = self.path.parent / name

    def move(self, new_path: str):
        self.path = Path(new_path)

    def read(self, base: str) -> str:
        with open(f"{base}/{self.path}", "r") as f:
            return f.read()
        
    def append(self, content: str):
        self.content += content

    def get_path(self) -> Path:
        return self.path