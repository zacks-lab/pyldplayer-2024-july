
from typing import TypedDict

class InstanceDict(TypedDict):
    id : int
    name : str
    top_window_handle : int 
    bind_window_handle : int
    android_started_int : int
    pid : int
    pid_of_vbox : int