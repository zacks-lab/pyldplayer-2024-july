
import typing

from pyldplayer.mapping._coord import Coord, TimingCoord
from pydantic import dataclasses

@dataclasses.dataclass
class KeyboardMap:
    extraData : str
    description : str
    moreDescription : str
    hintVisible : bool
    hintOffset : Coord

    @classmethod
    def create(cls, **data):
        if "class" not in data:
            return cls(**data)
        
        classtype = data["class"]
        data = data["data"]

        match classtype:
            case "ClassKeyboardDisc":
                return ClassKeyboardDisc(**data)
            case "ClassMouseTrigger":
                return ClassMouseTrigger(**data)
            case "ClassKeyboardCurve":
                return ClassKeyboardCurve(**data)
            case "ClassMouseODisc":
                return ClassMouseODisc(**data)
            case "ClassMouseMDisc":
                return ClassMouseMDisc(**data)
            case "ClassMouseDisc":
                return ClassMouseDisc(**data)
            case "ClassKeyboardMacros":
                return ClassKeyboardMacros(**data)
            case "ClassKeyboardPoint":
                return ClassKeyboardPoint(**data)
            case "ClassKeyboardGravity":
                return ClassKeyboardGravity(**data)
            case _:
                raise ValueError("Unknown class type")
            


# NOTE no needing inheritance
@dataclasses.dataclass
class ClassKeyboardDisc(KeyboardMap):
    origin : Coord
    leftKey : int
    upKey : int
    rightKey : int
    downKey : int

@dataclasses.dataclass
class ClassMouseTrigger(KeyboardMap):
    point : Coord

#NOTE base class
@dataclasses.dataclass
class KeyboardKey(KeyboardMap):
    key : int

@dataclasses.dataclass
class MultiKeyboardKey(KeyboardKey):
    secondKey : int

#NOTE Else
@dataclasses.dataclass
class ClassKeyboardCurve(MultiKeyboardKey):
    curve : typing.List[TimingCoord]

@dataclasses.dataclass
class ClassMouseODisc(KeyboardKey):
    origin : Coord
    sensitivity : int

@dataclasses.dataclass
class ClassMouseMDisc(KeyboardMap):
    type : int
    castMode : int
    waitRelease : bool
    noDirection : bool
    origin : Coord
    radius : int
    indicatorRadius : int

@dataclasses.dataclass
class ClassMouseDisc(ClassMouseMDisc):
    syntropyMove : bool
    synchronousMove : bool

@dataclasses.dataclass
class ClassKeyboardMacros(MultiKeyboardKey):
    macros : str
    origin : Coord

@dataclasses.dataclass
class ClassKeyboardPoint(MultiKeyboardKey):
    point : Coord
    type : int
    downDuration : int
    upDuration : int
    downDurationEx : int
    upDurationEx : int

@dataclasses.dataclass
class ClassKeyboardGravity(ClassKeyboardDisc):
    sensitivity : int