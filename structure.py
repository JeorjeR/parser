from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class HtmlTag:
    name: str
    content: list[str | Any]
    parent: Any | None

    def __repr__(self):
        return f'<{self.name}> {self.content} </{self.name}>'
