from pyldplayer.process.process import BaseProcess
from pyldplayer.process.processVerifier import ProcessVerifier
import typing

class DefaultProcess(BaseProcess, ProcessVerifier):
    def __init__(self, path: str) -> None:
        BaseProcess.__init__(self, path)
        ProcessVerifier.__init__(self)
        
class ProcessContainer:
    def __init__(self, *arg, path : str = None, process : typing.Union[BaseProcess, typing.Type[BaseProcess]] = DefaultProcess) -> None:
        
        if len(arg) == 1:
            if isinstance(arg[0], str):
                path = arg[0]
            else:
                process = arg[0]

        if isinstance(process, typing.Type):
            self.__process = process(path)
        elif isinstance(process, BaseProcess):
            self.__process = process
        else:
            raise TypeError("query must be BaseProcess or BaseProcessInterface type")
        
    @property
    def process(self):
        return self.__process
    