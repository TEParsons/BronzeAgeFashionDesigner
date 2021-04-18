from colour import Color


class BaseColor(Color):
    """
    Subclass of Color which generates shades and allows these shades to be accessed by +- operators
    """
    @property
    def shades(self):
        # Make range
        out = []
        for n in range(-8, 8+1):
            # Get base HSL
            h, s, l = list(self.get_hsl())
            # Desaturate as n increases
            s = min(max(s - n/16, 0), 1)
            # Lighten as n increases
            l = min(max(l + n / 16, 0), 1)
            # Reassemble hsl and make a new colour
            out.append(BaseColor(hsl=(h, s, l)))
        # Return list of colours
        return out

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