from pathlib import Path
from pygame import image
from .._base import DyableSprite

# Get files
sprites = {}
for sprite in Path(__file__).parent.glob("*.png"):
    if not sprite.stem.endswith("_"):
        sprites[sprite.stem] = DyableSprite(str(sprite))
# Append files to module namespace according to filename
globals().update(sprites)
# Update module namespace
__all__ = ["__folder__"] + list(sprites)