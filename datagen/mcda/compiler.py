from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from lark import Lark, Token, Tree


class _Block():
    def __init__(self, kind: str, name: str, hook: str | None, body: list[str]) -> None:
        self.kind = kind
        self.name = name
        self.hook = hook
        self.body = body


class MCDACompiler():
    grammar_path = Path(__file__).parent / "grammar.lark"

    def __init__(self) -> None:
        with open(self.grammar_path) as f:
            self.header_parser = Lark(f.read(), parser="lalr")

    def compile_file(self, source_path: str | Path, output_dir: str | Path = "datapacks/mcda") -> None:
        source = Path(source_path).read_text()
        self.compile_string(source, output_dir)

    def compile_string(self, source: str, output_dir: str | Path = "datapacks/mcda") -> None:
        output_dir = Path(output_dir)
        blocks = self._tokenize(source)
        pack = self._build(blocks)
        self._write(pack, output_dir)

    def _tokenize(self, source: str) -> list[_Block]:
        blocks: list[_Block] = []
        lines = source.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if not line or line.startswith(";"):
                continue

            if line.startswith(".entity_tag "):
                name = line.removeprefix(".entity_tag ").strip().rstrip(" {")
                values: list[str] = []
                while i < len(lines):
                    cl = lines[i].strip()
                    i += 1
                    if cl == "}":
                        break
                    if cl and not cl.startswith(";"):
                        values.append(cl.strip(","))
                blocks.append(_Block("entity_tag", name, None, values))

            elif line.startswith(".tag "):
                parts = line.removeprefix(".tag ").split(None, 2)
                tag_type = parts[0]
                tag_name = (parts[1] if len(parts) > 1 else "").rstrip(" {")
                values = []
                while i < len(lines):
                    cl = lines[i].strip()
                    i += 1
                    if cl == "}":
                        break
                    if cl and not cl.startswith(";"):
                        values.append(cl.strip(",").strip('"'))
                blocks.append(_Block("tag", f"{tag_type}/{tag_name}", None, [tag_type, tag_name, *values]))

            elif line.startswith(".fn "):
                content = line.removeprefix(".fn ").strip()
                hook = None
                fn_name = content.rstrip(" {").strip()
                hook_match = re.search(r"\bhook\s+(\S+:\S+)", content)
                if hook_match:
                    fn_name = content[:hook_match.start()].strip()
                    hook = hook_match.group(1)

                body: list[str] = []
                brace_depth = content.count("{") - content.count("}")
                body_started = "{" in content
                while i < len(lines):
                    cl = lines[i]
                    i += 1
                    stripped = cl.strip()
                    if not stripped or stripped.startswith(";"):
                        continue
                    dc = stripped.count("{") - stripped.count("}")
                    if not body_started and dc == -1 and stripped.strip() == "}":
                        break
                    if not body_started:
                        if "{" in stripped:
                            body_started = True
                            before, _, after = stripped.partition("{")
                            if before.strip():
                                body.append(before.strip())
                            brace_depth = 1 + after.count("{") - after.count("}")
                            if after.strip() and after.strip() != "}":
                                body.append(after.strip())
                            if brace_depth <= 0:
                                break
                        continue
                    brace_depth += dc
                    if stripped.strip() == "}" and brace_depth <= 0:
                        break
                    body.append(stripped)
                    if brace_depth <= 0:
                        break

                blocks.append(_Block("fn", fn_name, hook, body))

            elif line.startswith(".loot_table ") or line.startswith(".advancement ") or line.startswith(".recipe "):
                kind, rest = line.split(None, 1)
                kind = kind.lstrip(".")
                parts = rest.split(None, 1)
                name = parts[0]
                path = parts[1].strip('"') if len(parts) > 1 else ""
                blocks.append(_Block(kind, name, None, [path]))

            elif line.startswith("."):
                try:
                    tree = self.header_parser.parse(line)
                    for child in tree.children:
                        actual = child.children[0] if child.data == "directive" else child # type: ignore
                        blocks.append(self._tree_to_block(actual)) # type: ignore
                except Exception as e:
                    raise SyntaxError(f"Error parsing line {i}: {line}\n{e}")

        return blocks

    def _val(self, node: Tree | Token) -> str:
        if isinstance(node, Token):
            return node.value
        if node.children:
            return self._val(node.children[0])
        return ""

    def _tree_to_block(self, tree: Tree) -> _Block:
        match tree.data:
            case "pack_decl":
                name = self._val(tree.children[0]).strip('"')
                fmt = self._val(tree.children[1])
                return _Block("pack", name, None, [fmt])
            case "ns_decl":
                return _Block("ns", self._val(tree.children[0]), None, [])
            case "objective_decl":
                name = self._val(tree.children[0])
                criterion = self._val(tree.children[1]) if len(tree.children) > 1 else "dummy"
                return _Block("objective", name, None, [criterion])
            case "team_decl":
                return _Block("team", self._val(tree.children[0]), None, [
                    self._val(tree.children[1]),
                    self._val(tree.children[2]).strip('"'),
                ])
            case _:
                raise ValueError(f"Unknown directive: {tree.data}")

    def _build(self, blocks: list[_Block]) -> dict[str, Any]:
        pack: dict[str, Any] = {
            "name": None,
            "format": None,
            "ns": None,
            "objectives": [],
            "teams": [],
            "entity_tags": {},
            "tags": {},
            "functions": [],
            "resources": [],
        }
        for block in blocks:
            match block.kind:
                case "pack":
                    pack["name"] = block.name
                    pack["format"] = int(block.body[0])
                case "ns":
                    pack["ns"] = block.name
                case "objective":
                    pack["objectives"].append({"name": block.name, "criterion": block.body[0]})
                case "team":
                    pack["teams"].append({"name": block.name, "color": block.body[0], "display": block.body[1]})
                case "entity_tag":
                    pack["entity_tags"][block.name] = block.body
                case "tag":
                    pack["tags"][block.name] = {"type": block.body[0], "name": block.body[1], "values": block.body[2:]}
                case "fn":
                    pack["functions"].append({"name": block.name, "hook": block.hook, "commands": block.body})
                case "loot_table" | "advancement" | "recipe":
                    res_type = block.kind
                    pack["resources"].append({"type": res_type, "name": block.name, "path": block.body[0]})
        return pack

    def _write(self, pack: dict[str, Any], output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        ns = pack["ns"] or pack["name"]
        ns_path = output_dir / "data" / ns

        (output_dir / "pack.mcmeta").write_text(
            json.dumps({"pack": {"pack_format": pack["format"], "description": ""}}, indent=2)
        )

        self._write_functions(pack, ns, output_dir, ns_path)
        self._write_objectives_and_teams(pack, ns, output_dir, ns_path)
        self._write_tags(pack, ns_path)
        self._write_resources(pack, ns_path)

    def _write_functions(self, pack: dict[str, Any], ns: str, output_dir: Path, ns_path: Path) -> None:
        for fn in pack["functions"]:
            fn_path = ns_path / "function" / f"{fn['name']}.mcfunction"
            fn_path.parent.mkdir(parents=True, exist_ok=True)
            content = "\n".join(fn["commands"])
            fn_path.write_text(content + "\n" if content else "")

        for fn in pack["functions"]:
            if fn["hook"]:
                tag_ns, _, tag_name = fn["hook"].partition(":")
                tag_dir = output_dir / "data" / tag_ns / "tags" / "function"
                tag_dir.mkdir(parents=True, exist_ok=True)
                tag_file = tag_dir / f"{tag_name}.json"
                values: list[str] = []
                if tag_file.exists():
                    values = json.loads(tag_file.read_text()).get("values", [])
                values.append(f"{ns}:{fn['name']}")
                tag_file.write_text(json.dumps({"values": values}, indent=2))

    def _write_objectives_and_teams(self, pack: dict[str, Any], ns: str, output_dir: Path, ns_path: Path) -> None:
        load_lines: list[str] = []
        for obj in pack["objectives"]:
            load_lines.append(f"scoreboard objectives add {obj['name']} {obj['criterion']}")
        for team in pack["teams"]:
            load_lines.append(f"team add {team['name']}")
            load_lines.append(f"team modify {team['name']} color {team['color']}")

        if load_lines:
            load_path = ns_path / "function" / "mcda_load.mcfunction"
            load_path.parent.mkdir(parents=True, exist_ok=True)
            load_path.write_text("\n".join(load_lines) + "\n")

            load_tag_dir = output_dir / "data" / "minecraft" / "tags" / "function"
            load_tag_dir.mkdir(parents=True, exist_ok=True)
            load_tag_file = load_tag_dir / "load.json"
            load_values: list[str] = []
            if load_tag_file.exists():
                load_values = json.loads(load_tag_file.read_text()).get("values", [])
            load_values.append(f"{ns}:mcda_load")
            load_tag_file.write_text(json.dumps({"values": load_values}, indent=2))

    def _write_tags(self, pack: dict[str, Any], ns_path: Path) -> None:
        for tag_name, values in pack["entity_tags"].items():
            tag_dir = ns_path / "tags" / "entity_type"
            tag_dir.mkdir(parents=True, exist_ok=True)
            (tag_dir / f"{tag_name}.json").write_text(json.dumps({"values": values}, indent=2))

        type_to_dir: dict[str, str] = {
            "items": "item", "blocks": "block", "functions": "function",
            "entity_types": "entity_type", "enchantments": "enchantment",
        }
        for tag_key, tag_data in pack["tags"].items():
            subdir = type_to_dir.get(tag_data["type"], tag_data["type"])
            tag_dir = ns_path / "tags" / subdir # type: ignore
            tag_dir.mkdir(parents=True, exist_ok=True)
            (tag_dir / f"{tag_data['name']}.json").write_text(json.dumps({"values": tag_data["values"]}, indent=2))

    def _write_resources(self, pack: dict[str, Any], ns_path: Path) -> None:
        type_to_subdir: dict[str, str] = {
            "loot_table": "loot_table", "advancement": "advancement", "recipe": "recipes",
        }
        for res in pack["resources"]:
            subdir = type_to_subdir.get(res["type"], res["type"])
            source_path = Path(res["path"])
            if not source_path.is_absolute():
                source_path = Path.cwd() / source_path
            json_content = source_path.read_text()
            res_file = ns_path / subdir / f"{res['name']}.json" # type: ignore
            res_file.parent.mkdir(parents=True, exist_ok=True)
            res_file.write_text(json_content)
