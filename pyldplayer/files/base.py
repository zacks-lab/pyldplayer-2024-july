from pydantic import BaseModel
from pyldplayer.utils import convert_to_flatten, flatten_to_nested
import json

class StaticJsonMethods:
    @staticmethod
    def loadJson(path):
        with open(path, "r") as f:
            return json.load(f)
        
    @staticmethod
    def loadJsonFlattened(path):
        with open(path, "r") as f:
            return flatten_to_nested(json.load(f))
        
    @staticmethod
    def saveJson(path, data):
        with open(path, "w") as f:
            json.dump(data, f)
        
    
    @staticmethod
    def saveJsonFlattened(path, data, model: type[BaseModel]):
        with open(path, "w") as f:
            json.dump(convert_to_flatten(data, model), f)


try:
    import orjson

    @staticmethod
    def loadJson(path):
        with open(path, "rb") as f:
            return orjson.loads(f.read())
    
    @staticmethod
    def loadJsonFlattened(path):
        with open(path, "rb") as f:
            return flatten_to_nested(orjson.loads(f.read()))
        
    @staticmethod
    def saveJson(path, data):
        with open(path, "wb") as f:
            f.write(orjson.dumps(data))
    @staticmethod
    def saveJsonFlattened(path, data, model: type[BaseModel]):
        with open(path, "wb") as f:
            f.write(orjson.dumps(convert_to_flatten(data, model)))

    # wrap static
    StaticJsonMethods.loadJson = loadJson
    StaticJsonMethods.loadJsonFlattened = loadJsonFlattened
    StaticJsonMethods.saveJson = saveJson
    StaticJsonMethods.saveJsonFlattened = saveJsonFlattened

except ImportError:
    pass