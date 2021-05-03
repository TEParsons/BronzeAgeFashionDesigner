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
        starting = list(self.images)[0]

        # Initialise object
        pygame.Surface.__init__(self, self.images[starting].get_size(), flags=pygame.SRCALPHA)

        # Set starting current
        self.current = starting


    @property
    def current(self):
        if hasattr(self, "_current"):
            return self._current

    @current.setter
    def current(self, value):
        # If given a dict, convert it to a string key
        if isinstance(value, dict):
            assert all(key in value for key in self.axes)
            styles = [value[key] for key in self.axes]
            value = "_".join(styles)
        # Validate
        assert isinstance(value, str)
        assert value in self.images
        # Set current as keyed image
        self._current = self.images[value]
        # Clear and reblit
        self.fill(empty)
        self.blit(self._current, (0, 0))

    def dye(self, color):
        for sprite in self.images.values():
            sprite.dye(color)
        self.fill(empty)
        self.blit(self.current, (0, 0))

    def next(self):
        styles = list(self.images.values())
        names = list(self.images)
        i = styles.index(self.current)
        self.current = names[i-1]