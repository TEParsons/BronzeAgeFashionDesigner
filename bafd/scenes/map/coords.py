from math import floor
from bafd.utils.window import vsize

def validate_coord(value):
    # Enforce list/tuple
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"Expecting coordinate value of type list or tuple, got {type(value).__name__}")
    # Enforce (x, y) format
    if not len(value) == 2:
        raise ValueError(f"Coordinate values must be a pair of values (x, y)")


class Coord:
    """A class to handle seamless conversion between map and screen coordinates"""
    def __init__(self, coord, mode="screen"):
        # Validate
        if mode not in ['map', 'screen']:
            raise ValueError(f"Invalid value {mode} for coordinate mode")
        # Set some default values
        self._map = (0, 0)
        self._screen = (0, 0)
        # Supply value to setter methods
        setattr(self, mode, coord)

    def __repr__(self):
        return f"<Coord object: map={self.map} screen={self.screen}>"

    @property
    def map(self):
        """Location of this coordinate on the map"""
        return self._map
    @map.setter
    def map(self, value):
        validate_coord(value)
        self._map = value
        # Calculate screen coords
        self._screen = (
            floor(value[0]*5-value[1]*5)+vsize[0]/2-4,
            floor(value[1]*4+value[0]*4)-vsize[1]/2-30
        )

    @property
    def screen(self):
        """Location of this coordinate on the screen"""
        return self._screen
    @screen.setter
    def screen(self, value):
        validate_coord(value)
        self._screen = value
        # Calculate map coords
        self._map = (
            floor(value[0]/5),
            floor(value[1]/4)
        )