import typing
from pydantic import BaseModel, dataclasses, field_validator
from pyldplayer.mapping._base import Coord, Resolution
from pyldplayer.mapping.kmp_key import KeyboardMap

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