import typing
from pydantic import Field, dataclasses
import json

@dataclasses.dataclass
class SMP:
    _instances : typing.ClassVar[typing.Dict[str, "SMP"]] = {}

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

    @classmethod
    def fromPath(cls, path : str):
        if path not in cls._instances:
            with open(path, "r") as f:
                rawdata = json.load(f)
            cls._instances[path] = cls(**rawdata)
        return cls._instances[path]