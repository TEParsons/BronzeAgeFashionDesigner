from pygame import Color
import re


class BaseColor(Color):
    """
    Subclass of Color which generates shades and allows these shades to be accessed by +- operators
    """
    def update(self, *args, **kwargs):
        Color.update(self, *args, **kwargs)
        # Clear cache and recalculate shades
        if hasattr(self, "_shades"):
            del self._shades

    @property
    def hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @hex.setter
    def hex(self, value):
        value = value or "#ffffff"
        assert isinstance(value, str)
        assert re.fullmatch(r"#?[\dAaBbCcDdEeFf]{6}", value)
        # Strip hashtag
        value = value.replace("#", "")
        # Split into three
        r, g, b = re.findall(r"..", value)
        # Integerise and set
        self.r = int(r, 16)
        self.g = int(g, 16)
        self.b = int(b, 16)
        self.a = 255

    @property
    def url(self):
        root = "https://coolors.co/"
        dark_shades = [shade.hex.strip("#") for shade in self.shades[:8]]
        light_shades = [shade.hex.strip("#") for shade in self.shades[8:]]
        return [root + "-".join(dark_shades), root + "-".join(light_shades)]

    @property
    def shades(self):
        # If value already cached, don't bother recalculating
        if hasattr(self, "_shades"):
            return self._shades
        # Make range
        self._shades = []
        for n in range(-8, 8+1):
            # Get base HSL
            h, s, l, a = list(self.hsla)
            # Desaturate as n increases
            s = min(max(s - n/16*100, 0), 100)
            # Lighten as n increases
            l = min(max(l + n/16*100, 0), 100)
            # Reassemble hsl and make a new colour
            new = BaseColor(0, 0, 0, 0)
            new.hsla = (h, s, l, a)
            self._shades.append(new)
        # Return list of colours
        return self._shades

    def __add__(self, other):
        # Can only be added to numbers
        assert isinstance(other, (int, float))
        # Clamp other value to an int between -8 and 8
        other = min(range(-8, 8+1), key=lambda x:abs(x-other))
        # Convert to a 0-based index
        other += 8
        # Return the corresponding shade
        return self.shades[other]

    def __sub__(self, other):
        # Can only be added to numbers
        assert isinstance(other, (int, float))
        # Add as negative
        return self + -other

    def __repr__(self):
        return self.hex