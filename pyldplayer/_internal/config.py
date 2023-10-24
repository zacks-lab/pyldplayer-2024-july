"""
this module loads a config file resided at the same directory of the script
"""
import json
import os
import typing

class ConfigSingleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

_script_path = os.path.abspath(__file__)
_script_dir = os.path.dirname(_script_path)
_empty = object()

class Config(dict, metaclass=ConfigSingleton):
    __config_path : str = os.path.join(_script_dir, "config.json")

    def update(self, data, wflag : bool = True):
        super().update(data)
        if wflag:
            self.__write_config()

    def __init__(self):
        self.__load_config()

    def __getitem__(self, key):
        return super().__getitem__(key)
    
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__write_config()

    def __delitem__(self, key):
        super().__delitem__(key)
        self.__write_config()

    def __write_config(self):
        with open(self.__config_path, "w") as f:
            json.dump(self, f)

    def __create_config(self):
        with open(self.__config_path, "w") as f:
            json.dump({}, f)

    def __load_config(self):
        if not os.path.exists(self.__config_path):
            self.__create_config()

        with open(self.__config_path, "r") as f:
            self.update(json.load(f), wflag=False)

    def getnset(self, key : str, default : typing.Any = _empty):
        if key in self and self[key] is not None:
            return self[key]
        
        if default is _empty:
            raise KeyError(f"key {key} not found")
        
        if callable(default):
            default = default()

        self[key] = default
        return default
    
    def clear(self):
        self.__create_config()

config = Config()

__all__ = [
    "config",
]