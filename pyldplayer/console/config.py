
from typing_extensions import TypedDict
import typing

class LDModifyConfigDict(TypedDict):
    resolution : typing.Optional[typing.Tuple[int, int, int]]
    cpu : typing.Optional[typing.Literal[1,2,3,4]]
    memory : typing.Optional[typing.Literal[512,1024,2048,4096,8192]]
    manufacturer : typing.Optional[str]
    model : typing.Optional[str]
    pnumber : typing.Optional[int]
    imei : typing.Optional[typing.Union[typing.Literal["auto"], str]]
    imsi : typing.Optional[typing.Union[typing.Literal["auto"], str]]
    simserial : typing.Optional[typing.Union[typing.Literal["auto"], str]]
    androidid : typing.Optional[typing.Union[typing.Literal["auto"], str]]
    mac : typing.Optional[typing.Union[typing.Literal["auto"], str]]
    autorotate : typing.Optional[bool]
    lockwindow : typing.Optional[bool]

    root : typing.Optional[bool]