
import os
from pyldplayer._internal import config
from pyldplayer.utils.process import subprocess_exec


class LDPlayerApp:
    def __init__(self, path : str = None):
        self.__path = path
        if self.__path is None:
            self.__path = config.get("console_dir")

    def multiplayer(self):
        subprocess_exec(os.path.join(self.__path, "dnmultiplayer.exe"), "")