import os
import psutil

def find_ldconsole():
    # detect process dnmultiplayerex.exe
    for proc in psutil.process_iter():
        if proc.name() == "dnmultiplayerex.exe":
            # get parent path
            apppath = os.path.dirname(proc.exe())
            parentpath = os.path.dirname(apppath)
            suspected_path = os.path.join(parentpath, "ldconsole.exe")
        elif proc.name() == "ldconsole.exe":
            suspected_path = os.path.dirname(proc.exe())
        elif proc.name() == "dnplayer.exe":
            apppath = os.path.dirname(proc.exe())
            suspected_path = apppath
        elif proc.name() == "dnmultiplayer.exe":
            apppath = os.path.dirname(proc.exe())
            suspected_path = apppath
        else:
            continue

        break

    if os.path.isdir(suspected_path) and os.path.exists(suspected_path):
        return suspected_path
    
    return None

try:
    import orjson
    JSON_PARSER = orjson
    def JSON_READ(path : str):
        with open(path, "rb") as f:
            return JSON_PARSER.loads(f.read())

    def JSON_WRITE(path : str, data):
        with open(path, "wb") as f:
            f.write(JSON_PARSER.dumps(data))

except ImportError:
    import json
    JSON_PARSER = json
    def JSON_READ(path : str):
        with open(path, "r") as f:
            return JSON_PARSER.load(f)
        
    def JSON_WRITE(path : str, data):
        with open(path, "w") as f:
            JSON_PARSER.dump(data, f)