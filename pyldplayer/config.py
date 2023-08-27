
from dataclasses import dataclass, field, InitVar
import typing

unknown_obj = object()
auto_obj = object()
@dataclass
class LDPlayerConfig:
    """
    LDPlayer configuration
    
    available options:

    - resolution : typing.Tuple[int, int, int]
    - cpu : typing.Literal[1,2,3,4]
    - memory : typing.Literal[512,1024,2048,4096,8192]
    - manufacturer : str
    - model : str
    - pnumber : int
    - imei : str
    - imsi : str
    - simserial : str
    - androidid : str
    - mac : str
    - autorotate : bool
    - lockwindow : bool

    auto available options:
    - imei
    - imsi
    - simserial
    - androidid
    - mac
    """

    AUTO : InitVar[typing.Any] = auto_obj
    resolution : typing.Tuple[int, int, int] = field(default=unknown_obj, compare=False)
    cpu : typing.Literal[1,2,3,4] = field(default=unknown_obj, compare=False)
    memory : typing.Literal[512,1024,2048,4096,8192] = field(default=unknown_obj, compare=False)
    manufacturer : str = field(default=unknown_obj, compare=False)
    model : str = field(default=unknown_obj, compare=False)
    pnumber : int = field(default=unknown_obj, compare=False)
    imei : str = field(default=unknown_obj, compare=False)
    imsi : str = field(default=unknown_obj, compare=False)
    simserial : str = field(default=unknown_obj, compare=False)
    androidid : str = field(default=unknown_obj, compare=False)
    mac : str = field(default=unknown_obj, compare=False)
    autorotate : bool = field(default=unknown_obj, compare=False)
    lockwindow : bool = field(default=unknown_obj, compare=False)

    @property
    def res(self):
        return self.resolution[0:2]
    
    @property
    def dpi(self):
        return self.resolution[-1]
    
    def toCommand(self):
        commandstr = []

        for name in self.__dataclass_fields__.keys():
            if name == "AUTO":
                continue

            if (val := getattr(self, name)) is unknown_obj:
                continue
            elif val is auto_obj:
                commandstr += [f"--{name}", "auto"]
            elif isinstance(val, typing.Tuple):
                commandstr += [f"--{name}", ",".join(map(str, val))]
            elif not isinstance(val, bool):
                commandstr += [f"--{name}", str(val)]
            elif val:
                commandstr += [f"--{name}", "1"]
            else:
                commandstr += [f"--{name}", "0"]

        return commandstr
