from typing import TypedDict

class WidthHeight(TypedDict):
    width: int
    height: int 

class Hotkey(TypedDict):
    modifiers: int
    key : int

class XY(TypedDict):
    x: int
    y: int