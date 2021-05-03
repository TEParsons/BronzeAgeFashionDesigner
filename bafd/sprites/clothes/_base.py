import pygame
import numpy
from pathlib import Path
from collections import OrderedDict
from bafd.utils.colours import empty, BaseColor


class DyableSprite(pygame.Surface):
    def __init__(self, sprite):
        # Read in image
        assert isinstance(sprite, (Path, str))
        sprite = Path(sprite)
        # Set base image
        self.base = pygame.image.load(str(sprite))
        # Set dyable surface
        self.overlay = pygame.Surface(self.base.get_size(), flags=pygame.SRCALPHA)
        # Initialise object
        pygame.Surface.__init__(self, self.base.get_size(), flags=pygame.SRCALPHA)
        # Read in array of dyable region
        self.shades = numpy.loadtxt(
            sprite.parent / (sprite.stem + ".csv"),
            dtype=int
        )
        # Reset
        self.refresh()

    def refresh(self):
        # Clear surface then blit base image and overlay
        self.fill(empty)
        self.blit(self.base, (0, 0))
        self.blit(self.overlay, (0, 0))

    def dye(self, color):
        assert isinstance(color, (BaseColor, type(None)))

        # If dye is None, clear all dye
        if color is None:
            self.overlay.fill(empty)
            self.refresh()
            return
        # Get array of shades
        shades = [numpy.array([shade.r, shade.g, shade.b]) for shade in color.shades]
        # Dye pixels in shade map according to shades array
        overlay_color = pygame.surfarray.pixels3d(self.overlay)
        for i in range(-8, 8+1):
            # Skip shades not represented
            if not overlay_color[self.shades == i].shape[0]:
                continue
            overlay_color[self.shades == i] = shades[i+8]
        del overlay_color
        # Set alpha of overlay
        overlay_alpha = pygame.surfarray.pixels_alpha(self.overlay)
        overlay_alpha[:, :] = (self.shades != 99) * 255
        del overlay_alpha
        # Blit
        self.refresh()


class Garment(pygame.Surface):
    def __init__(self, path, axes):
        # Store path
        assert isinstance(path, (Path, str))
        path = Path(path)
        assert path.is_dir()
        self.path = path
        files = list(path.glob("*[!_].png"))

        assert len(files) > 0

        # Create dict of {axis: [values]} from axis names and filenames
        self.axes = OrderedDict(**{axis: [] for axis in axes})
        for i, axis in enumerate(axes):
            # For each axis, get all values represented in filenames
            values = []
            for file in files:
                value = file.stem.split("_")[i]
                if value not in values:
                    values.append(value)
            self.axes[axis] = values

        # Get files
        self.images = {}
        for file in files:
            self.images[file.stem] = DyableSprite(file)
        self.styles = list(self.images)

        # Initialise object
        pygame.Surface.__init__(self, self.images[self.styles[0]].get_size(), flags=pygame.SRCALPHA)

        # Set starting current
        self.style = self.styles[0]

    def clear(self):
        self.fill(empty)

    def update(self):
        self.clear()
        self.blit(self.image, (0, 0))

    @property
    def image(self):
        return self.images[self.style]

    @property
    def style(self):
        if hasattr(self, "_style"):
            return self._style

    @style.setter
    def style(self, value):
        # If given a dict, convert it to a string key
        if isinstance(value, dict):
            assert all(key in value for key in self.axes)
            styles = [value[key] for key in self.axes]
            value = "_".join(styles)
        # Validate
        assert isinstance(value, str)
        assert value in self.images
        # Set style as keyed image
        self._style = value

    @property
    def dye(self):
        if hasattr(self.image, "_dye"):
            return self.image._dye

    @dye.setter
    def dye(self, color):
        for sprite in self.images.values():
            sprite.dye(color)

    def next(self):
        # Find current index
        i = list(self.images.values()).index(self.image)
        # If at end of array, go to start
        if i+1 > len(self.styles)-1:
            i = -1
        # Set style to next value
        self.style = self.styles[i+1]

    def prev(self):
        # Find current index
        i = list(self.images.values()).index(self.image)
        # Set style to previous value
        self.style = self.styles[i-1]