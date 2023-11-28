
from pydantic import BaseModel
import typing
import json

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
    _instances : typing.ClassVar[typing.Dict[str, "Record"]] = {}

    operations : typing.List[typing.Union[PutMultiTouch, PutScanCode]]
    recordInfo : RecordInfo

    @classmethod
    def fromPath(cls, path : str):
        if path not in cls._instances:
            with open(path, "r") as f:
                rawdata = json.load(f)
            cls._instances[path] = cls(**rawdata)
        return cls._instances[path]