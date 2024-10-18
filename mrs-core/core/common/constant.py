from enum import Enum, auto
from typing import Any, List


class StrEnum(str, Enum):
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[Any]) -> Any:
        return name

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.name
