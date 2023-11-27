
from pydantic import BaseModel
import typing

class Point(BaseModel):
    id: int
    x: int
    y: int
    state: int

class PutMultiTouch(BaseModel):
    timing: int
    operationId: str
    points: typing.List[Point]

class PutScanCode(BaseModel):
    timing: int
    operationId: str
    code : int
    down : bool

class RecordInfo(BaseModel):
    loopType: int
    loopTimes: int
    circleDuration: int
    loopInterval: int
    loopDuration: int
    accelerateTimes: int
    accelerateTimesEx: int
    recordName: str
    createTime: str
    playOnBoot: bool
    rebootTiming: int

class Record(BaseModel):
    operations : typing.List[typing.Union[PutMultiTouch, PutScanCode]]
    recordInfo : RecordInfo