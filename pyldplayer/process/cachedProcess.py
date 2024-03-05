
import datetime
from typing import List
from pyldplayer.process.process import BaseProcess


class CachedProcess(BaseProcess):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.__cache = {}

    @property
    def cacheDriver(self):
        return self.__cache
    
    @cacheDriver.setter
    def cacheDriver(self, value):
        self.__cache = value

    def queryRaw(self, *args, timeout: int = 5):
        pres = super().queryRaw(*args, timeout=timeout)

        self.__cache[datetime.datetime.now()] = pres
        return pres

    def query(self, *args, timeout: int = 5, raw: bool = False, returnCtx: bool = False, decodeOrder: List[str] = ..., toList: bool = False, stripNullLines: bool = False):
        pres =  super().query(
            *args, timeout=timeout, raw=raw, returnCtx=returnCtx, decodeOrder=decodeOrder, toList=toList, stripNullLines=stripNullLines
        )

        self.__cache[datetime.datetime.now()] = pres

        return pres
    

