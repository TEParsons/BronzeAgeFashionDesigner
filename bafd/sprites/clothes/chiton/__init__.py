from pathlib import Path
from pygame import image

# Get files
sprites = {}
for sprite in Path(__file__).parent.glob("*.png"):
    sprites[sprite.stem] = image.load(str(sprite))
# Append files to module namespace according to filename
globals().update(sprites)
# Update module namespace
__all__ = ["__folder__"] + list(sprites)