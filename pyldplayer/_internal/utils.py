import psutil
import os

overlooking_processes = ["dnmultiplayerex.exe", "dnplayer.exe", "dnmultiplayer.exe"]

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

        if process.name() not in overlooking_processes:
            continue

        suspected_directory = os.path.dirname(process.exe())

        if process.name() == overlooking_processes[0]:
            suspected_directory = os.path.dirname(suspected_directory)

        suspected_path =os.path.join(suspected_directory, "ldconsole.exe")

        if not os.path.exists(suspected_path):
            return None

        return suspected_path

    return None