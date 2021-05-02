import pygame
import numpy
from pathlib import Path
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


class CompoundSprite(pygame.Surface):

    def __init__(self, path, axes):
        # Store path
        assert isinstance(path, (Path, str))
        path = Path(path)
        assert path.is_dir()
        self.path = path

        # Make key dicts
        self.axes = axes
        self.styles = {axis: [] for axis in self.axes}
        for file in path.glob("*.png"):
            for i, val in enumerate(file.stem.split("_")):
                if val not in self.styles[self.axes[i]]:
                    self.styles[self.axes[i]].append(val)
        # Get files
        self.surfaces = numpy.empty([len(keys) for keys in self.styles.values()],
                                    dtype=object)
        for file in path.glob("*.png"):
            ii = []
            for i, val in enumerate(file.stem.split("_")):
                ii.append(
                    self.styles[self.axes[i]].index(val)
                )
            self.surfaces[tuple(ii)] = pygame.image.load(str(file))

        # Initialise object
        pygame.Surface.__init__(self, (100, 100))


    def get(self, **kwargs):
        assert list(self.styles) == list(dict(kwargs))
        assert all(val in self.styles[key] for key, val in kwargs.items())
        ii = []
        for axis, val in kwargs.items():
            ii.append(
                self.styles[axis].index(val)
            )
        return self.surfaces[tuple(ii)]

    @property
    def current(self):
        if hasattr(self, "_current"):
            return self.get(**self._current)

    @current.setter
    def current(self, value):
        assert isinstance(value, dict)

        self._current = value