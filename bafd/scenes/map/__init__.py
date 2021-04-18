from pathlib import Path
import numpy
import pygame

from bafd.sprites import map as sprites
from .coords import Coord
from .tiles import Tile
from . import dialog, land, appeal, influence

__folder__ = Path(__file__).parent


class Map(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)

        self.tiles = numpy.ndarray(shape=land.landmap.shape, dtype=numpy.object_)
        # Placeholder coord object
        point = Coord((0, 0), mode="map")
        # Iterate through all coords
        for x, vals in enumerate(land.landmap):
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
        self.update_overlay()

    def update_overlay(self):
        for row in self.tiles:
            for cell in row:
                if isinstance(cell, Tile):
                    cell.update_overlay()
        pygame.display.update()