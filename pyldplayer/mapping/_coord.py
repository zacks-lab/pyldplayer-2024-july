from typing_extensions import TypedDict


class Coord(TypedDict):
    x : int
    y : int

class TimingCoord(Coord):
    timing : int
