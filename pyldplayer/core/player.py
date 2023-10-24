import typing

class LDInstance:
    def quit(self): 
        """
        quits the instance

        does nothing if the instance is not running
        """

    def launch(self): 
        """
        launches the instance

        does nothing if the instance is already running
        """

    def reboot(self): 
        """
        reboots the instance

        if instance is not running, throws error

        """

    @property
    def isrunning(self): 
        """ 
        returns true if the instance is running
        """

    def launchex(self, pkgname : str): 
        """
        Launches instance with specified package.

        will not launch if the instance is already running

        Args:
            pkgname (str): The name of the package to launch.
        """
        pass
        

INSTANCE_PARAM = typing.Union[str, int]

class LDPlayer:
    def quit(self, id : INSTANCE_PARAM): 
        """
        Quit the current session.

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
        pass

    def runninglist(self): 
        pass
    
    def list2(self): 
        pass

    def add(self): pass
    def copy(self): pass
    def remove(self): pass
    def rename(self): pass

    def operatelist(self): pass
    def operateinfo(self): pass
    def operaterecord(self): pass