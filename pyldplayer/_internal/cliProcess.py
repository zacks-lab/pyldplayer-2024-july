import os
import subprocess
import typing
from pyldplayer.utils.process import subprocess_exec
from pyldplayer.utils.process_finder import find_ldconsole
from pyldplayer._internal.config import config

class LDProcessMeta(type):
    _instances : typing.Dict[str, 'LDProcess'] = {}

    def __call__(cls, *args, **kw):
        path = kw.pop("path", None)
        if path is None and len(args) > 0:
            path = args[0]
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")
        
        if path not in cls._instances:
            cls._instances[path] = super().__call__(*args, **kw)

        return cls._instances[path]
            

class LDProcess(metaclass=LDProcessMeta):
    """
    used to connect to the dnconsole.exe cli
    """
    def __hash__(self) -> int:
        return hash(self.path)

    def __init__(self, path : str):
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")

        if not os.path.exists(path):
            raise RuntimeError("Could not find ldconsole.exe")
        
        self.path = path

    def instance_arg(self, instance : typing.Union[str, int]):
        if str(instance).isdigit():
            args = ["--index", str(instance)]
        else:
            args = ["--name", instance]

        return args


    def query(self, command : str, *args, timeout : int = 10):
        try:
            proc : subprocess.CompletedProcess = subprocess.run(
                [self.path, command, *args],
                capture_output=True,
                timeout=timeout
            )
            comm : bytes = proc.stdout

        except subprocess.TimeoutExpired as e:
            raise e
        except subprocess.CalledProcessError as e:
            raise e
        
        try:
            parsed = comm.decode("utf-8")
        except: # noqa
            parsed = comm.decode("gbk")
        
        # return stripped and splitted
        parsed = parsed.strip().split("\r\n")

        parsed = list(filter(None, parsed))
        parsed = list(map(lambda x: x.strip(), parsed))

        return parsed

    def exec(self, command : str, *args):
        subprocess_exec(self.path, command, *args)
        # todo logging    

_on_default_initialization : LDProcess = None

def _attempt_to_find_default():
    global _on_default_initialization

    try:
        # Get the path of the console executable
        path = config.getnset("console_path", find_ldconsole)
        config.getnset("console_dir", lambda: os.path.dirname(path))
        _on_default_initialization = LDProcess(path)
    except Exception:
        return

_attempt_to_find_default()


def ldprocess(path : str = None, set_global: bool = False):
    global _on_default_initialization
    if _on_default_initialization is None and path is None:
        raise RuntimeError("Could not find ldconsole.exe")
    
    if path is None:
        return _on_default_initialization
    
    proc = LDProcess(path)
    if set_global:
        
        _on_default_initialization = proc

    return proc

