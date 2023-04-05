from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class HtmlTag:
    name: str
    content: list
    parent: Any | None = None

    def __repr__(self):
        return f'<{self.name}> {self.content} </{self.name}>'
