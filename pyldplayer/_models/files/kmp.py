
from typing import List, Optional, TypedDict

from pydantic import BaseModel, Field

from pyldplayer._models.files.basic import XY, WidthHeight

class CurveItem(TypedDict):
    x: int
    y: int
    timing: int

class Data(BaseModel):
    type: Optional[int] = None
    origin: Optional[XY] = None
    radius: Optional[int] = None
    leftKey: Optional[int] = None
    upKey: Optional[int] = None
    rightKey: Optional[int] = None
    downKey: Optional[int] = None
    description: str
    moreDescription: str
    extraData: str
    hintVisible: bool
    hintOffset: XY
    key: Optional[int] = None
    secondKey: Optional[int] = None
    macros: Optional[str] = None
    curve: Optional[List[CurveItem]] = None
    point: Optional[XY] = None
    downDuration: Optional[int] = None
    upDuration: Optional[int] = None
    downDurationEx: Optional[int] = None
    upDurationEx: Optional[int] = None
    mode: Optional[int] = None
    sensitivity: Optional[int] = None
    sensitivity_y: Optional[int] = None
    sensitivityex_x: Optional[float] = None
    sensitivityex_y: Optional[float] = None

class KeyboardMapping(BaseModel):
    class_: str = Field(..., alias='class')
    data: Data

class ConfigInfo(BaseModel):
    version: int
    versionMessage: str
    packageNameType: int
    packageNamePattern: str
    resolutionType: int
    resolutionPattern: WidthHeight
    priority: int
    search: str

class KeyboardConfig(BaseModel):
    mouseCenter: XY
    mouseScrollType: int
    discType: int
    advertising: bool
    advertiseDuration: int
    advertiseText: str
    cancelPoint: XY
    cancelKey: int
    cancelMode: int
    cursor: str
    extraData: str

class KMP(BaseModel):
    keyboardMappings: List[KeyboardMapping]
    configInfo: ConfigInfo
    keyboardConfig: KeyboardConfig
