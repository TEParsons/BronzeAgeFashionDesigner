import pygame
from ... import sprites
from ...utils.ui import Button, ContainerMixin
from ...utils.colours import BaseColor, palette, empty


class Designer(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.blit(sprites.clothes.studio, (0, 0))

        self.dyes = DyePanel((5, 5), (50, 150))
        self.blit(self.dyes, self.dyes.pos)

        self.mannequin = Mannequin((90, 5))
        self.mannequin.clothing['top'].set(sprites.clothes.chiton.both_high_short)
        self.mannequin.dress()
        self.blit(self.mannequin, self.mannequin.pos)

    def on_click(self, pos):
        if pos in self.dyes:
            self.dyes.on_click(pos)


class Mannequin(pygame.Surface, ContainerMixin):
    def __init__(self, pos):
        ContainerMixin.__init__(self, pos, sprites.clothes.mannequin.get_size())
        pygame.Surface.__init__(self, self.size, flags=pygame.SRCALPHA)
        self.clothing = {
            'top': Clothing(pos=(0, 60), size=(self.w, self.h-70))
        }
        self.dress()

    def clear(self):
        self.fill(empty)
        self.blit(sprites.clothes.mannequin, (0, 0))

    def dress(self):
        self.clear()
        for item in self.clothing.values():
            self.blit(item, item.pos)

class Clothing(pygame.Surface, ContainerMixin):
    def __init__(self, pos, size):
        ContainerMixin.__init__(self, pos, size)
        pygame.Surface.__init__(self, size, flags=pygame.SRCALPHA)
        self.pos = pos
        self.size = size
        self._dye = None

    def clear(self):
        self.fill(empty)

    def set(self, sprite):
        self.clear()
        self.blit(sprite, (0, 0))
        self.dye(self._dye)

    def dye(self, dye):
        assert isinstance(dye, (BaseColor, type(None)))
        self._dye = dye
        if dye is None:
            return




class DyeButton(Button):
    dyes = {
        sprites.dyes.red: palette.red,
        sprites.dyes.orange: palette.orange,
        sprites.dyes.yellow: palette.yellow,
        sprites.dyes.green: palette.green,
        sprites.dyes.indigo: palette.indigo,
        sprites.dyes.purple: palette.purple,
        sprites.dyes.brown: palette.brown,
    }

    @property
    def dye(self):
        return self.dyes[self.image]

    def on_click(self, pos):
        print(self.dye.get_rgb())


class DyePanel(pygame.Surface, ContainerMixin):
    def __init__(self, pos, size):
        pygame.Surface.__init__(self, size, flags=pygame.SRCALPHA)
        self.pos = pos
        self.size = size

        self.buttons = {
            "red": DyeButton(sprites.dyes.red, (0, 00)),
            "orange": DyeButton(sprites.dyes.orange, (0, 20)),
            "yellow": DyeButton(sprites.dyes.yellow, (0, 40)),
            "green": DyeButton(sprites.dyes.green, (0, 60)),
            "indigo": DyeButton(sprites.dyes.indigo, (0, 80)),
            "purple": DyeButton(sprites.dyes.purple, (0, 100)),
            "brown": DyeButton(sprites.dyes.brown, (0, 120)),
        }
        self.fill(empty)
        for button in self.buttons.values():
            self.blit(button, button.pos)

    def on_click(self, pos):
        for button in self.buttons.values():
            if pos in button:
                button.on_click(pos)