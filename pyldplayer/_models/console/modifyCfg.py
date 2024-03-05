from typing import TypedDict, NotRequired, Tuple, Literal, Union

class ModifyCfg(TypedDict, total=False):
    resolution: NotRequired[Tuple[int, int, int]]
    cpu: NotRequired[Literal[1, 2, 3, 4]]
    memory: NotRequired[Literal[512, 1024, 2048, 4096, 8192]]
    manufacturer: NotRequired[str]
    model: NotRequired[str]
    pnumber: NotRequired[int]
    imei: NotRequired[Union[Literal["auto"], str]]
    imsi: NotRequired[Union[Literal["auto"], str]]
    simserial: NotRequired[Union[Literal["auto"], str]]
    androidid: NotRequired[Union[Literal["auto"], str]]
    mac: NotRequired[Union[Literal["auto"], str]]
    autorotate: NotRequired[bool]
    lockwindow: NotRequired[bool]
    root: NotRequired[bool]
