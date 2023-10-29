"""
this module is splitted from console_instance.py and console_player.py for better 
readability | project clarity

this module sets up instances and players to make sure only one instance of the same LDProcess
will be initialized
"""

from dataclasses import dataclass
import typing

from pyldplayer._internal.cliProcess import LDProcess

class LDConsoleMeta(type):
    __instance_mapping : typing.Dict[LDProcess, typing.Dict[int, 'LDConsoleInstanceI']] = {}

    def _resolve_list2(
        self, 
        itype : typing.Type['LDConsoleInstanceI'], 
        proc : LDProcess
    ):
        res = proc.query("list2")
        if not res:
            return
        # parse
        result = []

        for line in res:
            if not line:
                continue

            instance = itype(
                proc=proc,
                **dict(zip([
                    "id",
                    "name", 
                    "top_window_handle", 
                    "bind_window_handle",
                    "android_started_int", 
                    "pid", 
                    "pid_of_vbox",
                ], line.split(","))
                )
            )

            object.__setattr__(instance, "_LDConsoleInstance__proc", proc)
            result.append(instance)

        return result

    def __resolve_call_instance(self, *args, **kwds):
        proc = kwds.pop("proc", None)
        if proc is None and not isinstance(args[0], LDProcess):
            raise TypeError("Missing proc argument")
        if proc is None:
            proc = args[0]
            args = args[1:]

        if proc not in self.__instance_mapping:
            self.__instance_mapping[proc] = {}
        
        id = kwds.pop("id")
        if id not in self.__instance_mapping[proc]:
            self.__instance_mapping[proc][id] = super().__call__(
                id=id,
                **kwds
            )
            return self.__instance_mapping[proc][id]
        
        instance = self.__instance_mapping[proc][id]
        for k, v in kwds.items():
            if k not in LDConsoleInstanceI.__dataclass_fields__.keys():
                raise ValueError(f"unknown kwarg: {k}")
            object.__setattr__(instance, k, v)

        return instance

    def __call__(self, *args, **kwds) -> typing.Union['LDConsoleInstanceI', 'LDConsolePlayerI']:
        if issubclass(self, LDConsolePlayerI):    
            return super().__call__(*args, **kwds)
        else:
            return self.__resolve_call_instance(*args, **kwds)
        
class LDConsolePlayerI(metaclass=LDConsoleMeta):
    __proc : LDProcess

    def __init__(self, proc : LDProcess):
        self._LDConsolePlayer__proc = proc

    def list2(self)-> typing.List['LDConsoleInstanceI']:
        return self.__class__._resolve_list2(LDConsoleInstanceI, self._LDConsolePlayer__proc)

@dataclass(frozen=True)
class LDConsoleInstanceI(metaclass=LDConsoleMeta):
    id : int
    name : str
    top_window_handle : int
    bind_window_handle : int
    android_started_int : int
    pid : int
    pid_of_vbox : int
    
    def refresh(self):
        self.__class__._resolve_list2(
            self.__class__,self._LDConsoleInstance__proc
        )