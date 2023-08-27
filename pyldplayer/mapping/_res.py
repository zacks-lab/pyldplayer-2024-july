
from pydantic import dataclasses

@dataclasses.dataclass
class Resolution:
    width: int
    height: int