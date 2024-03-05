
import typing

from pyldplayer._models.console.modifyCfg import ModifyCfg


class ConsoleInstanceInterface:
    def quit(self): pass

    def launch(self): pass

    def reboot(self): pass

    def isrunning(self): pass

    def copy(self, name : str = None): pass

    def remove(self): pass

    def rename(self, name : str): pass

    def modify(self, **kwargs : typing.Unpack[ModifyCfg]): pass

    def installapp(self, filename : str = None, packagename : str = None): pass

    def uninstallapp(self, packagename : str = None): pass

    def runapp(self, packagename : str): pass

    def killapp(self, packagename : str): pass

    def locate(self, lng : str, lat : str): pass

    def adb(self, command : str, raw : bool = False): pass

    def setprop(self, key : str, value : str): pass

    def getprop(self, key : str): pass

    def downcpu(self, rate : int): pass

    def backup(self, filepath : str): pass

    def restore(self, filepath : str): pass

    def action(self, key : str, value : str): pass

    def scan(self, filepath : str): pass

    def pull(self, remote : str, local : str): pass

    def push(self, local : str, remote : str): pass

    def backupapp(self, filepath : str): pass

    def restoreapp(self, filepath : str): pass

    def launchex(self, packagename : str): pass

    def operatelist(self): pass

    def operaterecord(self, content : str): pass

InstanceInterfaceMethods = [
    "quit",
    "launch",
    "reboot",
    "isrunning",
    "copy",
    "remove",
    "rename",
    "modify",
    "installapp",
    "uninstallapp",
    "runapp",
    "killapp",
    "locate",
    "adb",
    "setprop",
    "getprop",
    "downcpu",
    "backup",
    "restore",
    "action",
    "scan",
    "pull",
    "push",
    "backupapp",
    "restoreapp",
    "launchex",
    "operatelist",
    "operaterecord"
]