
from functools import cache
import os
import subprocess
import typing
from pyldplayer.utils.process_finder import find_ldconsole
from pyldplayer._internal.config import config

class LDProcess:
    """
    used to connect to the dnconsole.exe cli
    """
    def __init__(self, path : str):
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
        
        parsed = comm.decode("utf-8")
        return parsed

    def exec(self, command : str, *args):
        proc = subprocess.Popen( # noqa
            [self.path, command, *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            creationflags=
                subprocess.DETACHED_PROCESS |
                subprocess.CREATE_NEW_PROCESS_GROUP | 
                subprocess.CREATE_BREAKAWAY_FROM_JOB
        )
        # todo logging    

_global_process = None

@cache
def ldprocess(set_global: LDProcess = None, raise_e: bool = False):
    """
    Initializes and returns the LDProcess object for the current session.

    Args:
        set_global (LDProcess): The LDProcess object to be set as the global process. 
            If None, the global process will attempt to be initialized.
        raise_e (bool): Whether to raise an exception if an error occurs during initialization.

    Returns:
        LDProcess: The initialized LDProcess object for the current session.
    """
    global _global_process

    if set_global is not None:
        _global_process = set_global
        return _global_process

    if _global_process is not None:
        return _global_process

    try:
        # Get the path of the console executable
        path = config.getnset("console_path", find_ldconsole)

        if not os.path.exists(path):
            raise RuntimeError("Could not find ldconsole.exe")

        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")

        # Initialize the global process object
        _global_process = LDProcess(path)
    except Exception as e:
        if raise_e:
            raise e
    
    return _global_process

ldprocess()