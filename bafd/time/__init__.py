from pygame import time


class Year:
    def __init__(self, value, length, map=None):
        assert isinstance(value, int)

        self._value = value
        self.length = length # length of a year in s
        self.clock = time.Clock() # internal clock
        self.time = 0
        self.map = map

    def check(self):
        self.clock.tick()
        self.time += self.clock.get_time()
        if self.time/1000 > self.length:
            self += 1
            print(self.time/1000)
            self.time = 0

    def __str__(self):
        christ = "AD" if self._value >= 0 else "BC"
        return f"{abs(self._value)} {christ}"

    def __int__(self):
        return self._value

    def __iadd__(self, other):
        assert isinstance(other, int)
        self._value += other
        if self.map:
            self.map.advance_year()
        return self

    def __isub__(self, other):
        self += -other
        return self

    def __eq__(self, other):
        assert isinstance(other, (int, float, Year))
        return self._value == int(other)