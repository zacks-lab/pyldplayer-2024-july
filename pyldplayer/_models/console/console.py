import typing

class ConsoleInterface:
    def quit(self, id : typing.Union[str, int]): pass

    def quitall(self): pass

    def launch(self, id : typing.Union[str, int]): pass

    def reboot(self, id : typing.Union[str, int]): pass

    def list(self): pass

    def runninglist(self): pass

    def isrunning(self, id : typing.Union[str, int]): pass

    def list2(self): pass

    def add(self, name : str): pass

    def copy(self, id : typing.Union[str, int], name : str = None): pass

    def remove(self, id : typing.Union[str, int]): pass

    def rename(self, id : typing.Union[str, int], name : str): pass

    def modify(self, id : typing.Union[str, int], **kwargs): pass

    def installapp(self, id : typing.Union[str, int], filename : str = None, packagename : str = None): pass

    def uninstallapp(self, id : typing.Union[str, int], packagename : str): pass

    def runapp(self, id : typing.Union[str, int], packagename : str): pass

    def killapp(self, id : typing.Union[str, int], packagename : str): pass

    def locate(self, id : typing.Union[str, int], lng : str, lat : str): pass

    def adb(self, id : typing.Union[str, int], command : str): pass

    def setprop(self, id : typing.Union[str, int], key : str, value : str): pass

    def getprop(self, id : typing.Union[str, int], key : str): pass

    def downcpu(self, id : typing.Union[str, int], rate : int): pass

    def backup(self, id : typing.Union[str, int], filepath : str): pass

    def restore(self, id : typing.Union[str, int], filepath : str): pass

    def action(self, id : typing.Union[str, int], key : str, value : str): pass

    def scan(self, id : typing.Union[str, int], filepath : str): pass

    def sortwnd(self): pass

    def zoomin(self): pass

    def zoomout(self): pass

    def pull(self, id : typing.Union[str, int], remote : str, local : str): pass

    def push(self, id : typing.Union[str, int], local : str, remote : str): pass

    def backupapp(self, id : typing.Union[str, int], filepath : str): pass

    def restoreapp(self, id : typing.Union[str, int], filepath : str): pass

    def globalsetting(
        self, 
        fps : int = None,
        audio : bool = None, 
        fastplay : bool = None, 
        cleanmode : bool = None
    ): pass

    def launchex(self, id : typing.Union[str, int], packagename : str): pass

    def operatelist(self, id : typing.Union[str, int]): pass

    def operateinfo(self, id : typing.Union[str, int], file : str): pass

    def operaterecord(self, id : typing.Union[str, int], content : str): pass
    
