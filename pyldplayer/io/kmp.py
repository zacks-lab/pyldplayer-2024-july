import dataclasses
import typing
from pydantic import BaseModel, field_validator
from typing_extensions import TypedDict

class Coord(TypedDict):
    x : int
    y : int

class TimingCoord(Coord):
    timing : int

class Resolution(TypedDict):
    width: int
    height: int
    
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
            case "ClassMouseDrag":
                return ClassMouseDrag(**data)
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


@dataclasses.dataclass
class ClassMouseDrag(ClassMouseODisc):
    mode : int
    sensitivity_y : int


@dataclasses.dataclass
class LDKMConfigInfo:
    version : int
    versionMessage : str
    packageNameType : int
    packageNamePattern : str
    resolutionType : int
    resolutionPattern : Resolution
    priority : int
    search : str

@dataclasses.dataclass
class LDKMKeyboardConfig:
    mouseCenter : Coord
    mouseScrollType : int
    discType : int
    advertising : bool
    advertiseDuration : int
    advertiseText : str
    cancelPoint : Coord
    cancelKey : int
    cancelMode : int
    cursor : str
    extraData : str

class LDKeyboardMapping(BaseModel):
    keyboardMappings : typing.List[KeyboardMap]
    configInfo : LDKMConfigInfo
    keyboardConfig : LDKMKeyboardConfig

    @field_validator("keyboardMappings", mode="before")
    @classmethod
    def _validate_keyboard_mappings(cls, v):
        if not isinstance(v, list):
            raise ValueError("keyboardMappings must be a list")
        
        if len(v) == 0:
            raise ValueError("keyboardMappings must not be empty")
        
        ret =[]
        for data in v:
            mapObj = KeyboardMap.create(**data)
            ret.append(mapObj)

        return ret