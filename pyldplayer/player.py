
from dataclasses import dataclass
from functools import cached_property, wraps
import math
from typing import Any
import subprocess
import os
import warnings
import toml
import typing
import inspect
from pyldplayer.config import LDPlayerConfig
from pyldplayer.mapping.kmp import LDKeyboardMapping
from pyldplayer.mapping.record import Record
from pyldplayer.mapping.smp import SMP
from pyldplayer.utils import JSON_READ, find_ldconsole

_default = object()

class LDInterface:
    def quit(self): pass
    def quitAll(self): pass
    def launch(self): pass
    def reboot(self): pass
    # def list(self): pass
    # def runninglist(self): pass
    def isrunning(self): pass
    # def list2 : typing.Callable
    def add(self): pass
    def copy(self): pass
    # def remove(self): pass
    # def rename(self): pass
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
    # def sortWnd(self): pass
    # def zoomIn(self): pass
    # def zoomOut(self): pass
    # def rock(self): pass
    def pull(self): pass
    def push(self): pass
    def backupapp(self): pass
    def restoreapp(self): pass
    # def globalsetting(self): pass
    def launchex(self): pass
    # def operatelist(self): pass
    # def operateinfo(self): pass
    # def operaterecord(self): pass

    # ANCHOR extensions
    def adb_shell(self): pass

class LDPlayerMeta(type):
    _singleton = None
    _config : dict = None
    _instanceableCommands : typing.List[str] = None

    CONFIG_PATH = "config.toml"
    TIMEOUT =10
    RAISE_RUNTIME_ERROR = True
    
    @property
    def appPath(self):
        return self.config("path")

    @property
    def customizedConfigPath(self):
        return os.path.join(self.appPath, "vms", "customizeConfigs")

    @property
    def operationRecordPath(self):
        return os.path.join(self.appPath, "vms", "operationRecords")

    @property
    def recommendConfigsPath(self):
        return os.path.join(self.appPath, "vms", "recommendConfigs")

    @property
    def ldConsolePath(self):
        return os.path.join(self.appPath, "ldconsole.exe")

    # SECTION config

    def config(self, *keys : typing.List[str], default=_default):
        target = self._config
        for key in keys:
            if default is _default:
                target = target[key]
            else:
                target = target.get(key, _default)
                if target is _default:
                    return default
        return target
    
        
    def setConfig(self, *keys : typing.List[str], value):
        target = self._config
        for key in keys[:-1]:
            if not isinstance(target, dict):
                raise ValueError("Invalid key path")
            
            if key not in target:
                target[key] = {}

            target = target[key]

        target[keys[-1]] = value

    def saveConfig(self):
        if not os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "w") as f:
                toml.dump({}, f)

        with open(self.CONFIG_PATH, "r") as f:
            config = toml.load(f)
            config["pyldplayer"] = self._config

        with open(self.CONFIG_PATH, "w") as f:
            toml.dump(config, f)

    def load_config(self):
        if os.path.exists(self.CONFIG_PATH):
            with open(self.CONFIG_PATH, "r") as f:
                return toml.load(f).get("pyldplayer", {})
        else:
            return {}
    #!SECTION
    # SECTION prep
    def _prep_config(self):
        if self._config is not None:
            return 
        self._config = self.load_config()
        if "path" in self._config:
            pass
        else:
            self._config["path"] = find_ldconsole()
        
        self.saveConfig()
        if "path" not in self._config or self._config["path"] is None:
            raise ValueError("LDPlayer path not found")

    @staticmethod
    def _prep_instanceable_commands(cls):
        _instanceableCommands = []

        for name, method in inspect.getmembers(cls, inspect.isfunction):
            if name.startswith("_"):
                continue
            if name in _instanceableCommands:
                continue
            # check if it takes instance as first argument
            signature = inspect.signature(method)
            if len(signature.parameters) <= 1:
                continue

            first_param = list(signature.parameters.values())[1]
            if first_param.name == "instance":
                _instanceableCommands.append(name)

        return _instanceableCommands


    #!SECTION
    # SECTION misc
    def __new__(cls, *args: Any, **kwds: Any) -> Any:

        newcls = super().__new__(cls, *args, **kwds)
        cls._instanceableCommands = cls._prep_instanceable_commands(cls=newcls)

        return newcls

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self._singleton is None:
            self._prep_config()
            self._singleton = super().__call__(*args, **kwds)

        return self._singleton

    def _execute_command(self, *command, ignore_error=False):
        command = [str(x) for x in command]
        fullcommand = " ".join([self.ldConsolePath, *command])
        
        try:
            proc : subprocess.CompletedProcess = subprocess.run(
                args=fullcommand,
                stdout=subprocess.PIPE, 
                timeout=LDPlayer.TIMEOUT
            )
            
            comm : bytes = proc.stdout
        except subprocess.TimeoutExpired:
            raise RuntimeError("Failed to execute command: " + fullcommand)
        if proc.returncode != 0 and self.__class__.RAISE_RUNTIME_ERROR and not ignore_error:
            raise RuntimeError("Failed to execute command: " + fullcommand)
        elif proc.returncode != 0:
            return None
        
        parsed = comm.decode("utf-8")
        if "Android Debug Bridge" in parsed:
            raise RuntimeError("Failed to execute command, ADB error: " + " ".join(command))
    
        return parsed
    
    def _prep_args(self, instance : typing.Union[str, int]):
        if str(instance).isdigit():
            args = ["--index", str(instance)]
        else:
            args = ["--name", instance]

        return args

class LDPlayer(LDInterface, metaclass=LDPlayerMeta):

    #!SECTION
    # SECTION commands
    def quit(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "quit", 
            *self.__class__._prep_args(instance)
        )
    
    def quitAll(self):
        return self.__class__._execute_command("quitall")
    
    def launch(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "launch", 
            *self.__class__._prep_args(instance)
        )

    def reboot(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "reboot", 
            *self.__class__._prep_args(instance)
        )

    def list(self):
        return self.__class__._execute_command("list")
    
    def runninglist(self):
        shell_result =  self.__class__._execute_command("runninglist")
        if shell_result is None:
            return []

        # split by \r\n
        result = shell_result.split("\r\n")
        # remove empty strings
        result = list(filter(None, result))

        instances = self.list2()
        instances = {x.name: x for x in instances}

        # filter
        result = [x for y,x in instances.items() if y in result]

        return result
    
    def isrunning(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "isrunning", 
            *self.__class__._prep_args(instance)
        ) == "running"

    def list2(self):
        shell_result =  self.__class__._execute_command("list2")
        if shell_result is None:
            return []

        # split by \r\n
        result = shell_result.split("\r\n")
        # remove empty strings
        result = list(filter(None, result))

        # remove first line
        result = result[1:]

        # parse
        result = [
            LDInstance(**dict(zip([
                "id",
                "name", 
                "top_window_handle", 
                "bind_window_handle",
                "android_started_int", 
                "pid", 
                "pid_of_vbox", 
            ], line.split(",")))) for line in result
        ]

        return result

    def add(self, name :str):
        return self.__class__._execute_command(
            "add", 
            "--name", 
            name
        )
    
    def copy(self, instance : typing.Union[str, int], name : str):
        return self.__class__._execute_command(
            "copy", 
            "--name",
            name,
            "--from",
            instance
        )
    
    def remove(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "remove", 
            *self.__class__._prep_args(instance)
        )
    
    def rename(self, instance : typing.Union[str, int], name : str):
        return self.__class__._execute_command(
            "rename", 
            *self.__class__._prep_args(instance),
            "--title",
            name
        )
    
    def modify(self, instance : typing.Union[str, int], config : LDPlayerConfig):
        return self.__class__._execute_command(
            "modify",
            *self.__class__._prep_args(instance),
            *config.toCommand()
        )

    def installapp(self, instance : typing.Union[str, int], filename : str=None, packageName : str = None):
        if filename is not None and packageName is not None:
            raise ValueError("filename and packageName cannot be both specified")

        if not filename and not packageName:
            raise ValueError("filename and packageName cannot be both unspecified")

        file_args = []
        if filename is not None:
            file_args = ["--filename", filename]
        else:
            file_args = ["--packagename", packageName]

        return self.__class__._execute_command(
            "installapp",
            *self.__class__._prep_args(instance),
            *file_args
        )

    def uninstallapp(self, instance : typing.Union[str, int], packageName : str):
        return self.__class__._execute_command(
            "uninstallapp",
            *self.__class__._prep_args(instance),
            "--packagename",
            packageName
        )
    
    def runapp(self, instance : typing.Union[str, int], packageName : str):
        return self.__class__._execute_command(
            "runapp",
            *self.__class__._prep_args(instance),
            "--packagename",
            packageName
        )
    
    def killapp(self, instance : typing.Union[str, int], packageName : str):
        return self.__class__._execute_command(
            "killapp",
            *self.__class__._prep_args(instance),
            "--packagename",
            packageName
        )
    
    def locate(self, instance : typing.Union[str, int], lng : float, lat : float):
        return self.__class__._execute_command(
            "locate",
            *self.__class__._prep_args(instance),
            "--LLI",
            f"{lng},{lat}"
        )

    def adb(self, instance : typing.Union[str, int], command : str):
        return self.__class__._execute_command(
            "adb",
            *self.__class__._prep_args(instance),
            "--command",
            f"'{command}'"
        )

    def setprop(self, instance : typing.Union[str, int], key : str, value : str):
        return self.__class__._execute_command(
            "setprop",
            *self.__class__._prep_args(instance),
            "--key",
            f'"{key}"',
            "--value",
            f'"{value}"'
        )
    
    def getprop(self, instance : typing.Union[str, int], key : str):
        return self.__class__._execute_command(
            "getprop",
            *self.__class__._prep_args(instance),
            "--key",
            f'"{key}"'
        )
    
    def downcpu(self, instance : typing.Union[str, int], cpu : int):
        """
        cpu : 0-100
        """
        if cpu < 0 or cpu > 100:
            raise ValueError("CPU must be between 0 and 100")

        return self.__class__._execute_command(
            "downcpu",
            *self.__class__._prep_args(instance),
            "--cpu",
            cpu
        )

    def backup(self, instance : typing.Union[str, int], filepath : str):
        return self.__class__._execute_command(
            "backup",
            *self.__class__._prep_args(instance),
            "--file",
            filepath
        )
    
    def restore(self, instance : typing.Union[str, int], filepath : str):
        return self.__class__._execute_command(
            "restore",
            *self.__class__._prep_args(instance),
            "--file",
            filepath
        )
    
    def action(self, instance : typing.Union[str, int], key : str, value : str):
        return self.__class__._execute_command(
            "action",
            *self.__class__._prep_args(instance),
            "--key",
            f'"{key}"',
            "--value",
            f'"{value}"'
        )

    def scan(self, instance : typing.Union[str, int], filepath : str):
        return self.__class__._execute_command(
            "scan",
            *self.__class__._prep_args(instance),
            "--file",
            filepath
        )
    
    def sortWnd(self):
        return self.__class__._execute_command(
            "sortWnd",
        )

    def zoomIn(self):
        return self.__class__._execute_command(
            "zoomIn",
        )
    
    def zoomOut(self):
        return self.__class__._execute_command(
            "zoomOut",
        )
    
    def rock(self):
        return self.__class__._execute_command(
            "rock",
        )
    
    def pull(self, instance : typing.Union[str, int], remote : str, local : str):
        return self.__class__._execute_command(
            "pull",
            *self.__class__._prep_args(instance),
            "--remote",
            remote,
            "--local",
            local
        )
    
    def push(self, instance : typing.Union[str, int], local : str, remote : str):
        return self.__class__._execute_command(
            "push",
            *self.__class__._prep_args(instance),
            "--local",
            local,
            "--remote",
            remote
        )
    
    def backupapp(self, instance : typing.Union[str, int], packageName : str, filepath : str):
        return self.__class__._execute_command(
            "backupapp",
            *self.__class__._prep_args(instance),
            "--packagename",
            packageName,
            "--file",
            filepath
        )
    
    def restoreapp(self, instance : typing.Union[str, int], filepath : str):
        return self.__class__._execute_command(
            "restoreapp",
            *self.__class__._prep_args(instance),
            "--file",
            filepath
        )
    
    def globalsetting(self, fps : int = None, audio : bool = None, fastplay : bool = None, cleanmode : bool = None):
        args = []
        if fps is not None:
            if fps < 1 or fps > 60:
                raise ValueError("FPS must be between 10 and 60")

            args.extend(["--fps", fps])
        
        if audio is not None:
            args.extend(["--audio", "1" if audio else "0"])
        
        if fastplay is not None:
            args.extend(["--fastplay", "1" if fastplay else "0"])

        if cleanmode is not None:
            args.extend(["--cleanmode", "1" if cleanmode else "0"])


        return self.__class__._execute_command(
            "globalsetting",
            *args
        )
    
    def launchex(self, instance : typing.Union[str, int], packagename :str):
        return self.__class__._execute_command(
            "launchex",
            *self.__class__._prep_args(instance),
            "--packagename",
            packagename
        )
    
    def operatelist(self, instance : typing.Union[str, int]):
        return self.__class__._execute_command(
            "operatelist",
            *self.__class__._prep_args(instance)
        )
    
    def operateinfo(self, instance : typing.Union[str, int], file:str):
        return self.__class__._execute_command(
            "operateinfo",
            *self.__class__._prep_args(instance),
            "--file",
            file
        )

    def operaterecord(self, instance : typing.Union[str, int], jsonstring : str):
        return self.__class__._execute_command(
            "operaterecord",
            *self.__class__._prep_args(instance),
            "--content",
            f"'{jsonstring}'"
        )
    
    #!SECTION
    #SECTION File parse
    def getSMPS(
            self, 
            targetPath : typing.Literal["customizedConfig", "recommendedConfig"] = "customizedConfig",
            name : str = None
        )-> typing.Dict[str,SMP]:
        if targetPath == "customizedConfig":
            targetPath = self.__class__.customizedConfigPath
        elif targetPath == "recommendedConfig":
            targetPath = self.__class__.recommendConfigsPath
        else:
            raise ValueError("Invalid targetPath")

        ret_dict = {}
        for file in os.listdir(targetPath):
            if not file.endswith(".smp"):
                continue
            
            if name is not None and name.lower() not in file.lower():
                continue

            path = os.path.join(targetPath, file)
            raw = JSON_READ(path)
            ret_dict[path] = SMP(**raw)
        
        return ret_dict
    
    def getKMPS(
        self,
        targetPath : typing.Literal["customizedConfig", "recommendedConfig"] = "customizedConfig",
        name : str = None        
    
    ) -> typing.Dict[str, LDKeyboardMapping]:
        if targetPath == "customizedConfig":
            targetPath = self.__class__.customizedConfigPath
        elif targetPath == "recommendedConfig":
            targetPath = self.__class__.recommendConfigsPath
        else:
            raise ValueError("Invalid targetPath")

        ret_dict = {}
        for file in os.listdir(targetPath):
            if not file.endswith(".kmp"):
                continue
            if name is not None and name.lower() not in file.lower():
                continue
            
            path = os.path.join(targetPath, file)
            raw = JSON_READ(path)
            ret_dict[path] = LDKeyboardMapping(**raw)
        
        return ret_dict

    def getRecords(
        self,
        targetPath : typing.Literal["operationRecords"] = "operationRecords",
        name : str = None
    ) -> typing.Dict[str, typing.Any]:
        if targetPath == "operationRecords":
            targetPath = self.__class__.operationRecordPath
        else:
            raise ValueError("Invalid targetPath")

        ret_dict = {}
        for file in os.listdir(targetPath):
            if not file.endswith(".record"):
                continue
            if name is not None and name.lower() not in file.lower():
                continue
            
            path = os.path.join(targetPath, file)
            raw = JSON_READ(path)
            ret_dict[path] = Record(**raw)
        
        return ret_dict

class LDInstanceMeta(type):
    MAX_CONFIG_ERROR : int = 3

    _ldplayer_methods_str : list = []
    _ldplayer_methods_redirection : dict = {}
    def __new__(cls, *args: Any, **kwds: Any) -> Any:

        newcls = super().__new__(cls, *args, **kwds)
        for name, method in inspect.getmembers(newcls, inspect.isfunction):
            if name.startswith("_"):
                continue

            signature = inspect.signature(method)
            if len(signature.parameters) > 1:
                pass
            else:
                
                cls._ldplayer_methods_str.append(name)
        return newcls

    def _get_ldplayer_redirection_method(self, name : str):
        if name in self._ldplayer_methods_redirection:
            return self._ldplayer_methods_redirection[name]

        ldplayer_ins = LDPlayer()
        method = getattr(ldplayer_ins, name)

        def basewrap(instance):
            @wraps(method)
            def wrapper(*args, **kwargs):
                return method(instance.id, *args, **kwargs)
            return wrapper

        self._ldplayer_methods_redirection[name] = basewrap
    
        return basewrap


@dataclass
class LDInstance(LDInterface, metaclass=LDInstanceMeta):
    id : int
    name : str
    top_window_handle : int
    bind_window_handle : int
    pid : int
    pid_of_vbox : int
    android_started_int : int

    def __getattribute__(self, __name: str) -> typing.Union[typing.Callable[..., typing.Any], typing.Any]:
        if __name.startswith("_"):
            return super().__getattribute__(__name)
        
        if __name not in self.__class__._ldplayer_methods_str:
            return super().__getattribute__(__name)
        
        method = self.__class__._get_ldplayer_redirection_method(__name)
        return method(self)        
    
    def _get_resolution_and_dpi(self):
        dpi = self.getprop("ro.sf.lcd_density")
        dpi = int(dpi)
        try:
            resolution = self.adb(self.id,"wm size")
            resolution = resolution.split(" ")[-1].strip()
            resolution_xy = resolution.split("x")
            resolution_x = int(resolution_xy[0])
            resolution_y = int(resolution_xy[1])
        except: # noqa
            return None, None, dpi

        return resolution_x, resolution_y, dpi

    def _get_total_ram(self):
        """
        return in mb
        """

        ram_unparsed_in_gb = self.adb_shell(
            "cat /proc/meminfo | grep MemTotal | awk '{print $2/1048576}'"
        )
        ram_raw_float = float(ram_unparsed_in_gb)
        # take the ceiling of the ram
        ram = math.ceil(ram_raw_float)
        return ram *1024

        # returned data 

    def _get_manufacturer(self):
        return self.getprop(self.id, "ro.product.manufacturer")

    def _get_model(self):
        return self.getprop(self.id, "ro.product.model")
  

    _mapping = {
        "model" : _get_model,
        "manufacturer" : _get_manufacturer,
        "total_ram" : _get_total_ram,
        "resolution" : _get_resolution_and_dpi,
    }

    @cached_property
    def config(self):
        if not self.is_running:
            raise ValueError("Instance is not running")
        
        error_count =0
        build_dict = {}

        for key, func in self._mapping.items():
            try:
                build_dict[key] = func(self)

                if not (key == "resolution" and isinstance(build_dict[key], tuple)):
                    continue

                if build_dict[key][0] is None or build_dict[key][1] is None:
                    error_count += 1
                    continue
                    
            except: # noqa
                error_count += 1
                
            if error_count > self.__class__.MAX_CONFIG_ERROR and self.__class__.MAX_CONFIG_ERROR > 0:
                warnings.warn("Failed to get all properties, return prematurely")
                return LDPlayerConfig(**build_dict)
            
        return LDPlayerConfig(**build_dict)
    
    def refreshConfig(self):
        del self.__dict__["config"]
        return self.config
    
    @property
    def lazyIsRunning(self):
        return self.pid != 0
    