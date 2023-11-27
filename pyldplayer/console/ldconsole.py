import datetime
import subprocess
import os

class LDConsoleMeta(type):
    _instances : dict = {}

    def __call__(cls, *args, **kw):
        path = kw.get("path", None)
        if path is None and len(args) > 0:
            path = args[0]
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")

        if path not in cls._instances:
            cls._instances[path] = super().__call__(*args, **kw)

        return cls._instances[path]

class LDConsole(metaclass=LDConsoleMeta):
    def __hash__(self) -> int:
        return hash(self.path)

    def __init__(self, path : str):
        if path is None:
            raise RuntimeError("Could not find ldconsole.exe")

        if (
            not os.path.exists(path)
            or not os.path.isfile(path)
            or not os.path.basename(path) == "ldconsole.exe"
        ):
            raise ValueError("Invalid path")

        self.path = path

        query_res = self.query(record=False, no_filter=True)

        if query_res[0] != 'dnplayer Command Line Management Interface':
            raise RuntimeError("Invalid path")
        
        self.__query_history = {}
        self.query_history_limit = 50
        self.__exec_history = {}
        self.exec_history_limit = 50

    def handle_keyvars(self, **kwargs):
        args = []
        for k, v in kwargs.items():
            args.append(f"--{k}")
            args.append(v)
        return args

    def query(self, command : str= None, *args, timeout : int = 10, record : bool = True, no_filter : bool = False):
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

        if record:
            self.__query_history[datetime.datetime.now()] = queryed
            while len(self.__query_history) > self.query_history_limit:
                self.__query_history.popitem(last=False)

        return parsed
    
    def exec(self, command : str, *args):
        subprocess.Popen( # noqa
            [self.path, command, *args],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            creationflags=
                subprocess.DETACHED_PROCESS |
                subprocess.CREATE_NEW_PROCESS_GROUP | 
                subprocess.CREATE_BREAKAWAY_FROM_JOB
        )
        self.__exec_history[datetime.datetime.now()] = command
        while len(self.__exec_history) > self.exec_history_limit:
            self.__exec_history.popitem(last=False)
