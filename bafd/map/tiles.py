import pygame
from .influence import influence
from ..sprites import map as sprites
from .coords import Coord

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
        # Initialise an overlay for each culture
        self.overlays = {
            culture: getattr(sprites, culture).copy()
            for culture in influence
        }
        # Apply initial inluence overlays
        self.update_overlay()

    @property
    def influence(self):
        """Dict of values indicating the level of influence of each culture on this tile (0:1)"""
        return {culture: infmap[self.coords.map]
                for culture, infmap in influence.items()}

    @influence.setter
    def influence(self, value):
        # Validate
        assert isinstance(value, dict)
        assert all(culture in influence for culture in value)
        assert all(0 <= val <= 255 for val in value.values())
        # Set module-level influence map
        for culture, val in value.items():
            influence[culture] = val

    def update_overlay(self):
        # Reset tile
        self.surface.blit(sprites.land, (0, 0))
        # Overlay for each culture
        for culture, inf in self.influence.items():
            # Set overlay opacity
            self.overlays[culture].set_alpha(inf*255)
            # Merge
            self.surface.blit(self.overlays[culture], (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
