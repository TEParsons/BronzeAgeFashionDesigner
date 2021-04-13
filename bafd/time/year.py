class Year:
    def __init__(self, value):
        assert isinstance(value, int)

        self.value = value

    def __str__(self):
        christ = "AD" if value >= 0 else "BC"
        return f"{abs(value)} {christ}"

    def __int__(self):
        return self.value