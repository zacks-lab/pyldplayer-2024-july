
from pyldplayer.autogui.instance import LDAutoInstance
from pyldplayer.console.player import LDConsolePlayer
import typing

class LDAutoPlayer:
    def __init__(self, ldplayer : LDConsolePlayer) -> None:
        self.__player = ldplayer

    def __getitem__(self, id : typing.Union[str, int]) -> LDAutoInstance:
        instance = self.__player[id]
        return LDAutoInstance(instance)