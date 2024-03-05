import typing
from pydantic import Field, dataclasses

@dataclasses.dataclass(slots=True)
class SMP:
    reduceInertia: bool = True
    keyboardShowGreet: bool = True
    joystickShowGreet: bool = True
    keyboardFirstGreet: bool = True
    joystickFirstGreet: bool = True
    keyboardShowHints: bool = True
    joystickShowHints: bool = True
    keyboardIgnoreVersion : int =0
    joystickIgnoreVersion: int = 0
    noticeTimes : int = 0
    noticeHash : int = 0
    resolutionRelatives : typing.Dict[str ,dict] = Field(default_factory=dict)