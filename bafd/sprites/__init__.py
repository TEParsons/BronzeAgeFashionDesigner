from pygame import image
from pathlib import Path

from . import metals, dyes, map, clothes, ui

logo = image.load(str(Path(__file__).parent / "logo.png"))