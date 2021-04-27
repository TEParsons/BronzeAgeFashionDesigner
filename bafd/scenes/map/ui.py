import pygame
from bafd.sprites import map as sprites
from bafd.utils.window import vsize

class TileDlg:
    def __init__(self, win, tile=None):

        self.surface = pygame.Surface((200, 300))
        self.tile = tile
        self.win = win
        self.populate()

    def populate(self):
        if self.tile is None:
            # If no tile assigned, just hide the dlg
            self.surface.set_alpha(0)
            return
        # Validate
        assert isinstance(self.tile, Tile)

        # Make sure dlg is shown
        self.surface.set_alpha(1)
        # Set background
        self.surface.fill((255, 255, 255))

        self.win.blit(self.surface, (0,0))#(vsize[0] * 0.65, vsize[1] * 0.05))

