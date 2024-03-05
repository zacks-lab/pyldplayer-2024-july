

from pyldplayer._models.console.console import ConsoleInterface
from pyldplayer._models.console.modifyCfg import ModifyCfg
from pyldplayer.process.container import ProcessContainer
import typing
from pyldplayer._models.console.consoleInstance import ConsoleInstanceInterface, InstanceInterfaceMethods
from pyldplayer._models.process.instanceMeta import InstanceDict
from pyldplayer.process import BaseProcess
from time import sleep as slp

class ConsoleInstanceMeta(type):
    _instances : typing.Dict[typing.Tuple[BaseProcess, int], 'ConsoleInstance'] = {}

    def __call__(cls, idict : InstanceDict, console : 'Console'):
        """
        The __call__ function creates or retrieves a ConsoleInstanceMeta instance based on the provided idict and console parameters.

        Parameters:
            cls: Class reference
            idict: InstanceDict - dictionary containing instance data
            console: 'Console' - console instance

        Returns:
            instance: ConsoleInstanceMeta - created or retrieved instance
        """
        if (console.process, idict['id']) in cls._instances:
            res = cls._instances[(console.process, idict['id'])]
            if res._ConsoleInstance__idict != idict:
                res._ConsoleInstance__idict = idict
            return res
        
        instance = super(ConsoleInstanceMeta, cls).__call__(idict, console)
        cls._instances[(console.process, idict['id'])] = instance

        return instance

class ConsoleInstance(ConsoleInstanceInterface, metaclass=ConsoleInstanceMeta):
    def __init__(self, idict : InstanceDict, console : 'Console'):
        self.__idict = idict
        self.__console = console

    @property
    def id(self):
        return self.__idict['id']
    
    @property
    def name(self):
        return self.__idict['name']
    
    @property
    def top_window_handle(self):
        return self.__idict['top_window_handle']
    
    @property
    def bind_window_handle(self):
        return self.__idict['bind_window_handle']
    
    @property
    def android_started_int(self):
        return self.__idict['android_started_int']
    
    @property
    def pid(self):
        return self.__idict['pid']
    
    @property
    def pid_of_vbox(self):
        return self.__idict['pid_of_vbox']
    
    def __getattribute__(self, __name: str) -> typing.Any:
        if __name.startswith("_"):
            return object.__getattribute__(self, __name)

        if __name in self.__idict:
            return object.__getattribute__(self, __name)
        
        if __name not in InstanceInterfaceMethods:
            return object.__getattribute__(self, __name)
        
        return lambda *args, **kwargs: getattr(self.__console, __name)(*args, id=self.id,**kwargs)

    def refresh(self, sleep : float = 0.3):
        """
        Method to refresh the object with an optional sleep duration.

        Args:
            sleep (float): The duration to sleep, defaults to 0.3.

        Returns:
            self: The refreshed object.
        """
        if sleep > 0:
            slp(sleep)
        self.__console.list2()
        return self

class Console(ProcessContainer, ConsoleInterface):
    def __resolve_id(self, id : typing.Union[str, int]):
        args = []
        if isinstance(id, str):
            args.append("--name")
            args.append(id)
        else:
            args.append("--index")
            args.append(str(id))
        return args
    
    def __getitem__(self, id : typing.Union[str, int]):
        list2res = self.process.list2()
        for item in list2res:
            if item["id"] == id:
                return ConsoleInstance(item, self)
            
        raise KeyError


    def quit(self, id : typing.Union[str, int]): 
        self.process.exec("quit", *self.__resolve_id(id))

    def quitall(self):
        self.process.exec("quitall")

    def launch(self, id : typing.Union[str, int]):
        self.process.exec("launch", *self.__resolve_id(id))

    def reboot(self, id : typing.Union[str, int]):
        self.process.exec("reboot", *self.__resolve_id(id))

    def list(self):
        return self.process.query("list")

    def runninglist(self): 
        return self.process.query("runninglist")
    
    def isrunning(self, id : typing.Union[str, int]):
        res = self.process.query("isrunning", *self.__resolve_id(id))
        if res[0] == "stop":
            return False
        elif res[0] == "running":
            return True
        return res
    
    def list2(self) -> typing.List[ConsoleInstance]:
        ret = []
        list2res = self.process.list2()
        for item in list2res:
            ret.append(ConsoleInstance(item, self))
            
        return ret
    
    def add(self, name : str = None): 
        if name is None:
            return self.process.exec("add")
        else:
            return self.process.exec("add", "--name", name)

    def copy(self, id : typing.Union[str, int], name : str = None): 
        if name is None:
            return self.process.exec("copy", *self.__resolve_id(id))
        else:
            return self.process.exec("copy", *self.__resolve_id(id), "--name", name)

    def remove(self, id : typing.Union[str, int]):
        return self.process.exec("remove", *self.__resolve_id(id))

    def rename(self, id : typing.Union[str, int], name : str):
        return self.process.exec("rename", *self.__resolve_id(id), "--title", name)

    def modify(self, id : typing.Union[str, int], **kwargs : typing.Unpack[ModifyCfg]): 
        args = []
        for name in kwargs.keys():
            val = kwargs[name]
            if val == "auto":
                args += [f"--{name}", "auto"]
            elif isinstance(val, typing.Tuple):
                args += [f"--{name}", ",".join(map(str, val))]
            elif not isinstance(val, bool):
                args += [f"--{name}", str(val)]
            elif val:
                args += [f"--{name}", "1"]
            else:
                args += [f"--{name}", "0"]
        return self.process.exec("modify", *self.__resolve_id(id), *args)
    
    def installapp(self, id : typing.Union[str, int], filename : str = None, packagename : str = None):
        if filename is not None:
            return self.process.exec("installapp", *self.__resolve_id(id), "--filename", filename)
        elif packagename is not None:
            return self.process.exec("installapp", *self.__resolve_id(id), "--packagename", packagename)
        else:
            raise ValueError("filename or packagename is required")

    def uninstallapp(self, id : typing.Union[str, int], packagename : str): 
        return self.process.exec("uninstallapp", *self.__resolve_id(id), "--packagename", packagename)

    def runapp(self, id : typing.Union[str, int], packagename : str):
        return self.process.exec("runapp", *self.__resolve_id(id), "--packagename", packagename)

    def killapp(self, id : typing.Union[str, int], packagename : str):
        return self.process.exec("killapp", *self.__resolve_id(id), "--packagename", packagename)        

    def locate(self, id : typing.Union[str, int], lng : str, lat : str):
        return self.process.exec("locate", *self.__resolve_id(id), "--LLI", f"{lng},{lat}")

    def adb(self, id : typing.Union[str, int], command : str, raw : bool = False):
        return self.process.query("adb", *self.__resolve_id(id), "--command", command, leave_raw=raw)

    def setprop(self, id : typing.Union[str, int], key : str, value : str):
        return self.process.exec(
            "setprop", *self.__resolve_id(id), "--key", key, "--value", value
        )

    def getprop(self, id : typing.Union[str, int], key : str):
        return self.process.query("getprop", *self.__resolve_id(id), "--key", key)

    def downcpu(self, id : typing.Union[str, int], rate : int):
        # if not 0 -100
        if rate < 0 or rate > 100:
            raise ValueError("rate must be between 0 and 100")

        return self.process.exec("downcpu", *self.__resolve_id(id), "--rate", str(rate))

    def backup(self, id : typing.Union[str, int], filepath : str):
        return self.process.exec("backup", *self.__resolve_id(id), "--file", filepath)

    def restore(self, id : typing.Union[str, int], filepath : str):
        return self.process.exec("restore", *self.__resolve_id(id), "--file", filepath)

    def action(self, id : typing.Union[str, int], key : str, value : str):
        return self.process.exec("action", *self.__resolve_id(id), "--key", key, "--value", value)

    def scan(self, id : typing.Union[str, int], filepath : str):
        return self.process.exec("scan", *self.__resolve_id(id), "--file", filepath)

    def sortwnd(self):
        return self.process.exec("sortwnd")

    def zoomin(self): 
        return self.process.exec("zoomin")

    def zoomout(self): 
        return self.process.exec("zoomout")

    def pull(self, id : typing.Union[str, int], remote : str, local : str):
        return self.process.exec("pull", *self.__resolve_id(id), "--remote", remote, "--local", local)

    def push(self, id : typing.Union[str, int], local : str, remote : str): 
        return self.process.exec("push", *self.__resolve_id(id),"--remote", remote,  "--local", local,)

    def backupapp(self, id : typing.Union[str, int], filepath : str): 
        return self.process.exec("backupapp", *self.__resolve_id(id), "--file", filepath)

    def restoreapp(self, id : typing.Union[str, int], filepath : str): 
        return self.process.exec("restoreapp", *self.__resolve_id(id), "--file", filepath)

    def globalsetting(
        self, 
        fps : int = None,
        audio : bool = None, 
        fastplay : bool = None, 
        cleanmode : bool = None
    ): 
        """
        Sets the global settings for the application.

        :param fps: The frames per second to set. Must be an integer between 0 and 60.
        :type fps: int, optional
        :param audio: Indicates whether audio should be enabled. Defaults to None.
        :type audio: bool, optional
        :param fastplay: Indicates whether fast play should be enabled. Defaults to None.
        :type fastplay: bool, optional
        :param cleanmode: Indicates whether clean mode should be enabled. Defaults to None.
        :type cleanmode: bool, optional
        :return: The result of the execution of the "globalsetting" command.
        :rtype: str
        """
        args = []
        if fps is not None:
            # 0-60
            if fps < 0 or fps > 60:
                raise ValueError("fps must be between 0 and 60")
            args.append("--fps")
            args.append(str(fps))
        if audio is not None:
            args.append("--audio")
            args.append(str(int(audio)))
        if fastplay is not None:
            args.append("--fastplay")
            args.append(str(int(fastplay)))
        if cleanmode is not None:
            args.append("--cleanmode")
            args.append(str(int(cleanmode)))
        return self.process.exec("globalsetting", *args)

    def launchex(self, id : typing.Union[str, int], packagename : str): 
        return self.process.exec("launchex", *self.__resolve_id(id), "--packagename", packagename)

    def operatelist(self, id : typing.Union[str, int]): 
        return self.process.exec("operatelist", *self.__resolve_id(id))

    def operateinfo(self, id : typing.Union[str, int], file : str): 
        return self.process.exec("operateinfo", *self.__resolve_id(id), "--file", file)

    def operaterecord(self, id : typing.Union[str, int], content : str): 
        return self.process.exec("operaterecord", *self.__resolve_id(id), "--content", content)