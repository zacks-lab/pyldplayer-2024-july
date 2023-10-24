from dataclasses import dataclass
from typing import Any
import typing
from pyldplayer._internal.cliProcess import LDProcess
from pyldplayer._internal.meta import LDConsoleInstanceI

@dataclass(frozen=True)
class LDConsoleInstance(LDConsoleInstanceI):
    def __post_init__(self):
        self.__proc : LDProcess

    def info(self):
        for key in self.__dataclass_fields__.keys():
            print(f"{key}: {getattr(self, key)}")
    def quit(self): 
        """
        quits the instance

        does nothing if the instance is not running
        """
        return self.__proc.query("quit", *self.__proc.instance_arg(self.id))

    def launch(self): 
        """
        launches the instance

        does nothing if the instance is already running
        """
        return self.__proc.exec("launch", *self.__proc.instance_arg(self.id))

    def reboot(self): 
        """
        reboots the instance

        if instance is not running, throws error

        """
        return self.__proc.exec("reboot", *self.__proc.instance_arg(self.id))

    @property
    def isrunning(self): 
        """ 
        returns true if the instance is running
        """
        res = self.__proc.query("isrunning", *self.__proc.instance_arg(self.id))
        return res == "running"

    def launchex(self, pkgname : str): 
        """
        Launches instance with specified package.

        will not launch if the instance is already running

        Args:
            pkgname (str): The name of the package to launch.
        """
        return self.__proc.exec(
            "launchex", 
            *self.__proc.instance_arg(self.id), 
            "--packagename",
            pkgname
        )
    
    def rename(self, name : str):
        object.__setattr__(self, "name", name)
        return self.__proc.exec(
            "rename", 
            *self.__proc.instance_arg(self.id), 
            "--title",
            name
        )
    
