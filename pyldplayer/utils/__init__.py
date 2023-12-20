from functools import cache
import os
from pyldplayer._internal.models.kmp import LDKeyboardMapping
from pyldplayer._internal.models.record import Record
from pyldplayer._internal.models.smp import SMP
from pyldplayer.core.console_wrapper import LDConsoleWrapper
import psutil

_overlooking_processes = ["dnmultiplayerex.exe", "dnplayer.exe", "dnmultiplayer.exe"]

def find_ldconsole():
    """
    Find the path to the ldconsole.exe process.

    Returns:
        str: The path to the ldconsole.exe process if it is found.
        None: If the ldconsole.exe process is not found.
    """
    for process in psutil.process_iter():
        if process.name() == "ldconsole.exe":
            return process.exe()

        if process.name() not in _overlooking_processes:
            continue

        suspected_directory = os.path.dirname(process.exe())

        if process.name() == _overlooking_processes[0]:
            suspected_directory = os.path.dirname(suspected_directory)

        suspected_path =os.path.join(suspected_directory, "ldconsole.exe")

        if not os.path.exists(suspected_path):
            return None

        return suspected_path

    return None

@cache
def app_root_folder(ldw : LDConsoleWrapper):
    return os.path.dirname(ldw.path)

def smps(ldw : LDConsoleWrapper):
    res = {}
    tpath = os.path.join(app_root_folder(ldw), "vms", "customizeConfigs")
    for file in os.listdir(tpath):
        if file.endswith(".smp"):
            res[os.path.basename(file)] = SMP.fromPath(os.path.join(tpath, file))
            
    return res

def kmps(ldw : LDConsoleWrapper):
    res = {}
    tpath = os.path.join(app_root_folder(ldw), "vms", "customizeConfigs")
    for file in os.listdir(tpath):
        if file.endswith(".kmp"):
            res[os.path.basename(file)] = LDKeyboardMapping.fromPath(os.path.join(tpath, file))
            
    return res

def operationRecords(ldw : LDConsoleWrapper):
    res = {}
    tpath = os.path.join(app_root_folder(ldw), "vms", "operationRecords")
    for file in os.listdir(tpath):
        if file.endswith(".record"):
            res[os.path.basename(file)] = Record.fromPath(os.path.join(tpath, file))
            
    return res

def rawOperationRecords(ldw : LDConsoleWrapper):
    tpath = os.path.join(app_root_folder(ldw), "vms", "operationRecords")
    res = {}
    for file in os.listdir(tpath):
        if file.endswith(".record"):
            with open(os.path.join(tpath, file), "r") as f:
                res[os.path.basename(file)] = f.read()
                
    return res