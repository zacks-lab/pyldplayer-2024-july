
from functools import cached_property
import os
import subprocess
from typing import List

from pyldplayer._models.process.process import BaseProcessCtx, BaseProcessInterface
from pyldplayer._models.process.instanceMeta import InstanceDict

class BaseProcessMeta(type):
    _singletons = {}

    def __call__(cls, path :str):
        path = os.path.abspath(path)

        if path not in cls._singletons:
            cls._singletons[path] = super(BaseProcessMeta, cls).__call__(path)
        
        return cls._singletons[path]

class BaseProcess(BaseProcessInterface, metaclass=BaseProcessMeta):
    def __init__(self, path : str) -> None:
        self.__path = path
    
    @property
    def path(self):
        return self.__path
    
    @cached_property
    def vmFolder(self):
        return os.path.join(os.path.dirname(self.path), "vms")

    @cached_property
    def configFolder(self):
        return os.path.join(self.vmFolder, "config")

    @cached_property
    def customizeConfigsFolder(self):
        return os.path.join(self.vmFolder, "customizeConfigs")
    
    @cached_property
    def operationRecordsFolder(self):
        return os.path.join(self.vmFolder, "operationRecords")
    
    @cached_property
    def recommendConfigsFolder(self):
        return os.path.join(self.vmFolder,  "recommendConfigs")

    def exec(self, *args):
        """
        Execute a subprocess with the given arguments.

        Args:
            *args: Variable length argument list.

        Returns:
            None
        """
        subprocess.Popen( # noqa
        [self.path, *args],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=
            subprocess.DETACHED_PROCESS |
            subprocess.CREATE_NEW_PROCESS_GROUP | 
            subprocess.CREATE_BREAKAWAY_FROM_JOB
    )
        
    def queryRaw(self, *args, timeout : int = 5):
        """
        Executes a raw query using the specified arguments and a timeout.

        Args:
            *args: Any additional arguments for the query.
            timeout (int): The maximum time to wait for the query to complete (default is 5).

        Returns:
            bytes: The output of the query execution.
        """
        try:
            if not len(args):
                queryed = [self.path]
            else:
                queryed = [self.path, *args]

            proc : subprocess.CompletedProcess = subprocess.run(
                queryed,
                capture_output=True,
                timeout=timeout
            )
            comm : bytes = proc.stdout

        except subprocess.TimeoutExpired as e:
            raise e
        except subprocess.CalledProcessError as e:
            raise e
        
        return comm
    
    def query(
        self, 
        *args, 
        timeout: int = 5, 
        raw: bool = False, 
        returnCtx: bool = False, 
        decodeOrder: List[str] = ["utf-8", "gbk"], 
        toList: bool = False,
        stripNullLines : bool = False
    ):
        """
        Perform a query with optional parameters for timeout, raw output, return context, decoding order, conversion to list, and stripping null lines.

        Args:
            *args: Variable length argument list.
            timeout (int): Timeout duration in seconds (default is 5).
            raw (bool): Flag to indicate whether to return raw output (default is False).
            returnCtx (bool): Flag to indicate whether to return the context (default is False).
            decodeOrder (List[str]): List of encoding orders to decode raw output (default is ["utf-8", "gbk"]).
            toList (bool): Flag to indicate whether to convert the output to a list (default is False).
            stripNullLines (bool): Flag to indicate whether to strip null lines from the output (default is False).

        Returns:
            Union[str, BaseProcessCtx]: The processed query output, possibly with context information.
        """
        rawProcess = self.queryRaw(*args, timeout=timeout)

        if raw:
            return rawProcess
        
        for decoder in decodeOrder:
            try:
                decoded = rawProcess.decode(decoder)
            except: #noqa
                continue

            ret = decoded

        if toList:
            ret = ret.strip().split("\r\n")
        
            if stripNullLines:
                ret = list(filter(None, ret))
                ret = list(map(lambda x: x.strip(), ret))

        if returnCtx:
            flags = []
            if toList:
                flags.append("to_list")
            
            if stripNullLines:
                flags.append("strip_null")


            return BaseProcessCtx(
                final = ret,
                raw = rawProcess,
                decoded = decoded,
                flags = flags
            )
        
        return ret
    
    def list2(self) -> List[InstanceDict]:
        """
        A function to retrieve a list of InstanceDict objects from the database.
        This function queries the "list2" endpoint and processes the raw data into a list of InstanceDict objects.
        
        Returns:
            List[InstanceDict]: A list of InstanceDict objects containing the retrieved data.
        """
        raw : list = self.query("list2", toList=True)
        
        ret = []
        for item in raw:
            item : str
            splitted = item.split(",")

            ret.append(InstanceDict(
                id=int(splitted[0]),
                name=splitted[1],
                top_window_handle=int(splitted[2]),
                bind_window_handle=int(splitted[3]),
                android_started_int=int(splitted[4]),
                pid=int(splitted[5]),
                pid_of_vbox=int(splitted[6]),
            ))
        
        return ret
    
    def __hash__(self) -> int:
        return hash(self.path)