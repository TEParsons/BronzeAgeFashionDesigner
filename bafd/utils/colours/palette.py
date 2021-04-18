from ._base import BaseColor

# Base colours
red = BaseColor("#B5181E")
orange = BaseColor("#ED6D18")
yellow = BaseColor("#F4AB2A")
green = BaseColor("#205929")
blue = BaseColor("#2A3771")
purple = BaseColor("#5C3777")
brown = BaseColor("#8C3F20")
white = BaseColor("#DADCE0")
grey = BaseColor("#766B6B")
black = BaseColor("#131416")
# Coolors link
url = f"https://coolors.co/" \
      f"{red.get_hex_l()}-" \
      f"{orange.get_hex_l()}-" \
      f"{yellow.get_hex_l()}-" \
      f"{green.get_hex_l()}-" \
      f"{blue.get_hex_l()}-" \
      f"{purple.get_hex_l()}-" \
      f"{brown.get_hex_l()}-" \
      f"{white.get_hex_l()}-" \
      f"{grey.get_hex_l()}-" \
      f"{black.get_hex_l()}".replace("#", "")
# Colours for each culture
cultures = {
    'celtic': blue,
    'thracean': green,
    'italic': purple,
    'greek': purple+2,
    'hittite': yellow,
    'iberian': brown+2,
    'berber': brown,
    'lybian': red,
    'egyptian': orange,
}
cultures_lines = {culture: cultures[culture]-2
                  for culture in cultures}
