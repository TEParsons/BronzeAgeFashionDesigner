from pathlib import Path
from pygame import image

from ._base import Garment, DyableSprite

__folder__ = Path(__file__).parent

# Import basics
mannequin = image.load(str(__folder__ / "mannequin.png"))
studio = image.load(str(__folder__ / "studio.png"))

# Import garments
chiton = Garment(__folder__ / "chiton", ["shoulder", "belt", "length"])
alopekis = Garment(__folder__ / "alopekis", ["ears"])
