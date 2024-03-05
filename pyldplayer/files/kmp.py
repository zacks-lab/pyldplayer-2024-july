
import os
import typing
from pyldplayer._models.files.kmp import KMP
from pyldplayer.files.base import StaticJsonMethods
from pyldplayer.process.container import ProcessContainer

class KmpMgr(ProcessContainer, StaticJsonMethods):
    def customized(self):
        kmps=  []

        for file in os.listdir(self.process.customizeConfigsFolder):
            if not file.endswith(".kmp"):
                continue

            path = os.path.join(self.process.customizeConfigsFolder, file)

            kmps.append(KMP(**self.loadJson(path)))

        return kmps
        
    def recommended(self):
        kmps=  []

        for file in os.listdir(self.process.recommendConfigsFolder):
            if not file.endswith(".kmp"):
                continue

            path = os.path.join(self.process.customizeConfigsFolder, file)

            kmps.append(KMP(**self.loadJson(path)))

        return kmps

    def get(
        self, prefix : str = None, suffix : str = None, contains : str = None, 
        loc : typing.Literal["customize", "recommend"] = "customize",
        limit : int = 1
    ):
        target = self.process.recommendConfigsFolder if loc == "recommend" else self.process.customizeConfigsFolder

        for file in os.listdir(target):
            if not file.endswith(".kmp"):
                continue

            if prefix is not None and not file.startswith(prefix):
                continue

            if suffix is not None and not file.endswith(suffix):
                continue

            if contains is not None and contains not in file:
                continue

            path = os.path.join(target, file)

            data = self.loadJson(path)

            if limit == 1:
                return KMP(**data)
            
            limit -= 1
            if "ret" not in locals():
                ret = []
            ret.append(KMP(**data))

            if limit == 0:
                return ret
            
        return ret