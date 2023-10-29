from dataclasses import dataclass
import typing
from pyldplayer._internal.cliProcess import LDProcess, ldprocess
from pyldplayer._internal.meta import LDConsolePlayerI
from pyldplayer.core.instance import LDConsoleInstance

INSTANCE_PARAM = typing.Union[str, int]

class LDConsolePlayer(LDConsolePlayerI):
    @classmethod
    def create(cls, path : str = None):
        proc = ldprocess(path)
        return cls(proc=proc)

    @property
    def allInstances(self):
        return self.__class__.__class__.__instance_mapping[self.__proc]

    def getInstance(self, id : INSTANCE_PARAM):
        """
        Returns the instance with the given ID.
        """
        if isinstance(id, str):
            for instance in self.allInstances.values():
                if instance.name == id:
                    return instance
        else:
            return self.__class__._LDConsoleMeta__instance_mapping[self.__proc][str(id)]

    #ANCHOR
    def quit(self, id : INSTANCE_PARAM): 
        """
        end the current instance.

        Args:
            id (str, int): The identifier of the instance.

        Returns:
            None
        """
        pass

    def launch(self, id : INSTANCE_PARAM): 
        """
        Launches the specified instance.

        Args:
            id (str, int): The ID of the instance to be launched.

        Returns:
            None
        """
        pass

    def reboot(self, id : INSTANCE_PARAM): 
        """
        Reboots the specified instance.

        Args:
            id (str, int): The ID of the instance to reboot.

        Returns:
            None
        """
        pass

    def isrunning(self, id : INSTANCE_PARAM): 
        """
        Check if the instance with the given ID is running.

        Parameters:
            id (INSTANCE_PARAM): The ID of the instance to check.

        Returns:
            None
        """
        pass
    
    def modify(self): pass
    def installapp(self): pass
    def uninstallapp(self): pass
    def runapp(self): pass
    def killapp(self): pass
    def locate(self): pass
    def adb(self): pass
    def setprop(self): pass
    def getprop(self): pass
    def downcpu(self): pass
    def backup(self): pass
    def restore(self): pass
    def action(self): pass
    def scan(self): pass
    def sortWnd(self): pass
    
    def rock(self): pass
    def pull(self): pass
    def push(self): pass
    def backupapp(self): pass
    def restoreapp(self): pass
    
    def launchex(self, id : INSTANCE_PARAM, pkgname : str): 
        pass

    #ANCHOR - 
    def zoomIn(self): pass
    def zoomOut(self): pass

    def globalsetting(self, fps : int = None, audio : bool = None, fastplay : bool = None, cleanmode : bool = None): 
        pass

    def quitAll(self): 
        pass

    def list(self): 
        return self.__proc.query("list")

    def runninglist(self): 
        pass
    
    def list2(self)-> typing.List['LDConsoleInstance']:
        return self.__class__._resolve_list2(LDConsoleInstance, self.__proc)

    def add(self): pass
    def copy(self): pass
    def remove(self): pass
    def rename(self): pass

    def operatelist(self): pass
    def operateinfo(self): pass
    def operaterecord(self): pass