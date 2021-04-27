from pathlib import Path
import numpy
import pygame

from bafd.sprites import map as sprites
from bafd.utils.window import vsize
from ... import time
from . import spread

__folder__ = Path(__file__).parent

# Read csv of land/water tiles
landmap = numpy.fliplr(
    numpy.genfromtxt(__folder__ / 'land.csv', delimiter=',')
)


class Map(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)

        self.tiles = numpy.ndarray(shape=landmap.shape, dtype=numpy.object_)
        # Placeholder coord object
        point = Coord((0, 0), mode="map")
        # Iterate through all coords
        for x, vals in enumerate(landmap):
            for y, val in enumerate(vals):
                point.map = (x, y)
                if val == 1:
                    # If tile is land, style it according to influence maps
                    self.tiles[x, y] = Tile((x, y))
                    self.blit(self.tiles[x, y].surface, point.screen)
                elif val == 0:
                    # If tile is water, just draw it
                    self.tiles[x, y] = sprites.water
                    self.blit(self.tiles[x, y], point.screen)
        # Store neighbours
        for x, row in enumerate(self.tiles):
            for y, cell in enumerate(row):
                # Skip non-tiles
                if not isinstance(cell, Tile):
                    continue
                # Get nearby tiles
                near = self.tiles[x-1:x+1, y-1:y+1].flatten()
                for neighbour in near:
                    if isinstance(neighbour, Tile):
                        # Store non-None neighbours in tile attr
                        cell.neighbours.append(neighbour)
        # Set starting year
        self.year = time.Year(-1500, length=0.1, map=self)

    def advance_year(self):
        # Iterate through tiles
        for cell in self.tiles.flatten():
            if isinstance(cell, Tile):
                # Advance year on each cell
                cell.advance_year()
                # Reblit
                self.blit(cell.surface, cell.coords.screen)

    def on_click(self, pos):
        i = Coord(pos, mode="screen").map
        if hasattr(self.tiles[i], "on_click"):
            self.tiles[i].on_click(pos)


class Tile:
    def __init__(self, coords, resources=[]):
        # Validate
        if not isinstance(coords, Coord):
            coords = Coord(coords, mode="map")
        # Initialise surface
        self.surface = sprites.land.copy()
        # Store values given
        self.coords = coords
        self.resources = resources
        # Blank array to store neighbours in
        self.neighbours = []
        # Initialise an overlay for each culture
        self.overlays = {
            culture: getattr(sprites, culture).copy()
            for culture in spread.cultures
        }
        # Apply initial inluence overlays
        self.update_overlay()

    @property
    def demographics(self):
        """Demographic (cultural) makeup of this tile"""
        return spread.demographics[self.coords.map]

    @demographics.setter
    def demographics(self, value):
        # Validate
        assert isinstance(value, numpy.ndarray)
        assert value.dtype == self.demographics.dtype
        # Set
        spread.demographics[self.coords.map] = value

    @property
    def influence(self):
        """Cultural influence emitted by this tile"""
        return self.demographics

    def advance_year(self):
        """Progress by 1 year"""
        # Recalculate demographics of each culture according to influence of neighbours
        adj = numpy.array(
            [cell.influence for cell in self.neighbours],
            dtype=self.demographics.dtype
        )
        for culture in spread.cultures:
            spread.demographics[culture][self.coords.map] += numpy.nanmean(adj[culture]) * numpy.random.choice([0.9, 1, 1.1])
        # Re-normalise demographics
        total = sum(spread.demographics[self.coords.map])
        for culture in spread.cultures:
            spread.demographics[culture][self.coords.map] /= total
        # Update overlay
        self.update_overlay()

    def update_overlay(self):
        # Reset tile
        self.surface.blit(sprites.land, (0, 0))
        # Overlay for each culture
        for culture in spread.cultures:
            # Set overlay opacity
            self.overlays[culture].set_alpha(self.demographics[culture]*255)
            # Merge
            self.surface.blit(self.overlays[culture], (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)

    def on_click(self, pos):
        print(self.coords.map)


class Coord:
    """A class to handle seamless conversion between map and screen coordinates"""
    def __init__(self, coord, mode="screen"):
        # Validate
        if mode not in ['map', 'screen']:
            raise ValueError(f"Invalid value {mode} for coordinate mode")
        # Set some default values
        self._map = (0, 0)
        self._screen = (0, 0)
        # Supply value to setter methods
        setattr(self, mode, coord)

    def __repr__(self):
        return f"<Coord object: map={self.map} screen={self.screen}>"

    @property
    def map(self):
        """Location of this coordinate on the map"""
        return self._map

    @map.setter
    def map(self, value):
        # Validate
        assert isinstance(value, (list, tuple))
        assert len(value) == 2
        # Set value
        self._map = value
        # Calculate screen coords
        self._screen = (
            numpy.floor(value[0]*5-value[1]*5)+vsize[0]/2-4,
            numpy.floor(value[1]*4+value[0]*4)-vsize[1]/2-30
        )

    @property
    def screen(self):
        """Location of this coordinate on the screen"""
        return self._screen

    @screen.setter
    def screen(self, value):
        # Validate
        assert isinstance(value, (list, tuple))
        assert len(value) == 2
        # Set value
        self._screen = value
        # Calculate map coords
        self._map = (
            numpy.floor(value[0]/5),
            numpy.floor(value[1]/4)
        )