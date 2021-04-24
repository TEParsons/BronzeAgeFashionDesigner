from pygame import time
from bafd.scenes.map.influence import advance_year

class Year:
    def __init__(self, value, length):
        assert isinstance(value, int)

        self.value = value
        self.length = length # length of a year in s
        self.clock = time.Clock() # internal clock
        self.time = 0

    def check(self):
        self.clock.tick()
        self.time += self.clock.get_time()
        if self.time/1000 > self.length:
            self.time = 0
            self += 1

    def __str__(self):
        christ = "AD" if self.value >= 0 else "BC"
        return f"{abs(self.value)} {christ}"

    def __int__(self):
        return self.value

    def __iadd__(self, other):
        assert isinstance(other, int)
        # Do the actual addition
        self.value += other
        # Recalculate influence
        advance_year()
        return self

    def __isub__(self, other):
        self += -other
        return self

    def __eq__(self, other):
        assert isinstance(other, (int, float, Year))
        return self.value == int(other)