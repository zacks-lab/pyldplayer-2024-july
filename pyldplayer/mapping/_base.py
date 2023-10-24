from typing_extensions import TypedDict

class Coord(TypedDict):
    x : int
    y : int

class TimingCoord(Coord):
    timing : int

class Resolution(TypedDict):
    width: int
    height: int