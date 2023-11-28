
from functools import cached_property
import os
from pyldplayer.autogui.instance import LDAutoInstance
from pyldplayer.console.player import LDConsolePlayer
import typing
from pyldplayer.io.kmp import LDKeyboardMapping
from pyldplayer.io.record import Record

from pyldplayer.io.smp import SMP

class LDAutoPlayer:
    def __init__(self, ldplayer : LDConsolePlayer) -> None:
        self.__player = ldplayer

    def __getitem__(self, id : typing.Union[str, int]) -> LDAutoInstance:
        instance = self.__player[id]
        return LDAutoInstance(instance)
    
    @cached_property
    def __ldplayer_root_folder(self):
        dire = os.path.dirname(self.__player.path)
        return dire
    
    def smps(self):
        res = {}
        tpath = os.path.join(self.__ldplayer_root_folder, "vms", "customizeConfigs")
        for file in os.listdir(tpath):
            if file.endswith(".smp"):
                res[os.path.basename(file)] = SMP.fromPath(os.path.join(tpath, file))

    def kmps(self):
        res = {}
        tpath = os.path.join(self.__ldplayer_root_folder, "vms", "customizeConfigs")
        for file in os.listdir(tpath):
            if file.endswith(".kmp"):
                res[os.path.basename(file)] = LDKeyboardMapping.fromPath(os.path.join(tpath, file))

    def operationRecords(self):
        res = {}
        tpath = os.path.join(self.__ldplayer_root_folder, "vms", "operationRecords")
        for file in os.listdir(tpath):
            if file.endswith(".json"):
                res[os.path.basename(file)] = Record.fromPath(os.path.join(tpath, file))