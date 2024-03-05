import os
from pyldplayer._models.files.ledian_cfg import LeidianCfg
from pyldplayer._models.files.leidians_cfg import LeidiansCfg
from pyldplayer.files.base import StaticJsonMethods
from pyldplayer.process.container import  ProcessContainer
from pyldplayer.process.process import BaseProcess

class ConfigMgr(ProcessContainer, StaticJsonMethods):
    def __init__(self, *arg, path: str = None, query: BaseProcess | type[BaseProcess] = ...) -> None:
        super().__init__(*arg, path=path, query=query)

        if not os.path.exists(self.process.configFolder):
            raise RuntimeError("Could not find config folder")
        
        if not os.path.exists(os.path.join(self.process.configFolder, "leidians.config")):
            raise RuntimeError("Could not find leidians.config")

    def hostConfig(self):
        data =  self.loadJson(os.path.join(self.process.configFolder, "leidians.config"))
        return LeidiansCfg(**data)
    
    def profileConfig(self, id : int):
        data =  self.loadJsonFlattened(os.path.join(self.process.configFolder, f"leidian{id}.config"))
        return LeidianCfg(**data)

    def getAllProfiles(self):
        ret = {}
        for file in os.listdir(self.process.configFolder):
            if not file.endswith(".config"):
                continue
            
            if file.startswith("leidians"):
                continue
            data = self.loadJsonFlattened(os.path.join(self.process.configFolder, file))

            ret[file] = LeidianCfg(**data)
            
        return ret

    
    