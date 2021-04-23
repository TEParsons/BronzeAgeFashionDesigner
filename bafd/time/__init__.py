from pygame import time

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
            self.value += 1

    def __str__(self):
        christ = "AD" if self.value >= 0 else "BC"
        return f"{abs(self.value)} {christ}"

    def __int__(self):
        return self.value

    def __iadd__(self, other):
        assert isinstance(other, int)
        # Do the actual addition
        self.value += other
        # Recalculate


        return self

    def __isub__(self, other):
        self += -other
        return self