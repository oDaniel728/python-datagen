
from typing import Literal, TypedDict


class ClickEvent(TypedDict):
    action: Literal[
        "open_url",
        "open_file",
        "run_command",
        "suggest_command",
        "change_page",
        "copy_to_clipboard"
    ]
    value: str