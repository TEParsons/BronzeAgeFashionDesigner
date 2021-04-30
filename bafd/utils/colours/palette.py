from ._base import BaseColor

# Base colours
red = BaseColor("#B5181E")
orange = BaseColor("#ED6D18")
yellow = BaseColor("#F4AB2A")
green = BaseColor("#205929")
indigo = BaseColor("#2A3771")
purple = BaseColor("#5C3777")
brown = BaseColor("#8C3F20")
white = BaseColor("#DADCE0")
grey = BaseColor("#766B6B")
black = BaseColor("#131416")
# Coolors link
url = f"https://coolors.co/" \
      f"{red.hex}-" \
      f"{orange.hex}-" \
      f"{yellow.hex}-" \
      f"{green.hex}-" \
      f"{indigo.hex}-" \
      f"{purple.hex}-" \
      f"{brown.hex}-" \
      f"{white.hex}-" \
      f"{grey.hex}-" \
      f"{black.hex}".replace("#", "")
# Colours for each culture
cultures = {
    'celtic': indigo,
    'thracean': green,
    'greek': purple,
    'hittite': yellow,
    'iberian': brown+2,
    'berber': brown,
    'lybian': red,
    'egyptian': orange,
}
cultures_lines = {culture: cultures[culture]-2
                  for culture in cultures}
