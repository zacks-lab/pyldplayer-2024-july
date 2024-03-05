
import typing

class BaseProcessCtx(typing.TypedDict, total=False):
    final : typing.Union[str, typing.List[str]]
    raw : bytes
    decoded : typing.Optional[str]
    flags : typing.List[typing.Literal["leave_raw", "to_list"]]

class BaseProcessInterface:
    path : str

    def exec(self, *args):
        pass

    def queryRaw(self, *args, timeout : int = 5) -> bytes:
        pass
    
    def query(
        self, 
        *args,
        timeout : int = 5, 
        returnCtx : bool = False,
        raw : bool = False,
        decodeOrder : typing.List[str] = ["utf-8", "gbk"],
        toList : bool = False
    )-> typing.Union[BaseProcessCtx, bytes, str, typing.List[str], None]:
        pass