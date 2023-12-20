
import typing
import os
import subprocess
import datetime

class LDConsoleWrapperMeta(type):
    _instances : typing.ClassVar[typing.Dict[str, "LDConsoleWrapper"]] = {}
    
    def __call__(cls, path : str):
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")
        
        if not (
            os.path.exists(path)
            and os.path.isfile(path)
            and os.path.basename(path) == "ldconsole.exe"
        ):
            raise RuntimeError("Could not find ldconsole.exe")
        
        path = os.path.abspath(path)
        
        if path not in cls._instances:
            cls._instances[path] = super(LDConsoleWrapperMeta, cls).__call__(path)
        return cls._instances[path]
    
class LDConsoleWrapper(metaclass=LDConsoleWrapperMeta):
    """
    A class to manage and interact with the 'ldconsole.exe' command line interface.

    This class provides functionality to execute queries and commands on 'ldconsole.exe',
    and maintains a history of these operations. It ensures that only one instance of
    LDConsoleWrapper is created for each distinct path to 'ldconsole.exe'.

    ### Attributes:
        - _path_instances (typing.ClassVar[typing.Dict[str, "LDConsoleWrapper"]]): 
            Class-level dictionary holding instances of LDConsoleWrapper, indexed by their path.

    ### Properties:
        - query_history: Returns the history of queries executed.
        - exec_history: Returns the history of commands executed.

    ### Methods:
        - query(command: str, *args, timeout: int, no_filter: bool): 
            Executes a query command on ldconsole.exe and returns the output.
        - exec(command: str, *args): 
            Executes a command with the specified arguments on ldconsole.exe.

    ### Raises:
        - RuntimeError: If the 'ldconsole.exe' cannot be found or the path is invalid.
        - ValueError: If incorrect types are provided to properties.
        - subprocess.TimeoutExpired: If a query command times out.
        - subprocess.CalledProcessError: If there is an error in command execution.
    """
    
    def __init__(self, path : str):
        self.__query_history = None
        self.__exec_history = None
        self.max_history = 50
        
        self.path = path
        query_res = self.query(no_filter=True)

        if query_res[0] != 'dnplayer Command Line Management Interface':
            raise RuntimeError("Invalid path")
        
    @property
    def query_history(self):
        return self.__query_history
    
    @query_history.setter
    def __query_history_toggle(self, value : bool):
        if not isinstance(value, bool):
            raise ValueError("provided must be a bool")
        if value:
            self.__query_history = {} if self.__query_history is None else self.__query_history
        else:
            self.__query_history = None
            
    @property
    def exec_history(self):
        return self.__exec_history
    
    @exec_history.setter
    def __exec_history_toggle(self, value : bool):
        if not isinstance(value, bool):
            raise ValueError("provided must be a bool")
        if value:
            self.__exec_history = {} if self.__exec_history is None else self.__exec_history
        else:
            self.__exec_history = None
        
    def query(self, command : str= None, *args, timeout : int = 10, no_filter : bool = False):
        """
        Executes a query command and returns the parsed output as a list of strings.
        
        Args:
            command (str, optional): The query command to execute. If not provided, the default command will be used. 
            Defaults to None.
            *args: Additional arguments for the query command.
            timeout (int, optional): The maximum time to wait for the query command to complete, in seconds. 
            Defaults to 10.
            no_filter (bool, optional): Whether to filter out empty strings from the parsed output. Defaults to False.
        
        Returns:
            list: The parsed output of the query command as a list of strings.
        """
        try:
            if command is None:
                queryed = [self.path]
            else:
                queryed = [self.path, command, *args]

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
        
        try:
            parsed = comm.decode("utf-8")
        except: # noqa
            parsed = comm.decode("gbk")
        

        parsed = parsed.strip().split("\r\n")
        # return stripped and splitted
        if no_filter:
            parsed = list(filter(None, parsed))
            parsed = list(map(lambda x: x.strip(), parsed))

        if self.__query_history is None:
            return parsed
        
        self.__query_history[datetime.datetime.now()] = queryed
        while len(self.__query_history) > self.max_history:
            self.__query_history.popitem(last=False)

        return parsed
    
    def exec(self, command : str, *args):
        """
        Executes a command with the given arguments.

        Args:
            command (str): The command to be executed.
            *args (tuple): Additional arguments for the command.
        """
        subprocess.Popen( # noqa
            [self.path, command, *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            creationflags=
                subprocess.DETACHED_PROCESS |
                subprocess.CREATE_NEW_PROCESS_GROUP | 
                subprocess.CREATE_BREAKAWAY_FROM_JOB
        )
        
        if self.__exec_history is None:
            return
        
        self.__exec_history[datetime.datetime.now()] = command
        while len(self.__exec_history) > self.max_history:
            self.__exec_history.popitem(last=False)

    def __hash__(self) -> int:
        return hash(self.path)