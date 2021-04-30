import pygame
from ... import sprites
from ...utils.ui import Button, ContainerMixin
from ...utils.colours import BaseColor, palette, empty


class Designer(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.blit(sprites.clothes.studio, (0, 0))

        self.mannequin = Mannequin(self, (90, 5))
        self.mannequin.clothing['top'].set(sprites.clothes.chiton.both_high_short)
        self.mannequin.dress()

        self.dyes = DyePanel(self, (5, 5), (50, 150))
        self.blit(self.dyes, self.dyes.pos)

    def on_click(self, pos):
        if pos in self.dyes:
            self.dyes.on_click(pos)


class Mannequin(pygame.Surface, ContainerMixin):
    def __init__(self, parent, pos):
        ContainerMixin.__init__(self, pos, sprites.clothes.mannequin.get_size())
        pygame.Surface.__init__(self, self.size, flags=pygame.SRCALPHA)
        self.parent = parent
        self.clothing = {
            'top': Clothing(self, pos=(0, 60), size=(self.w, self.h-70))
        }
        self._current = 'top'
        self.dress()

    @property
    def current(self):
        return self.clothing[self._current]

    @current.setter
    def current(self, value):
        if value in self.clothing:
            self._current = value
        if value in self.clothing.values():
            for key, val in self.clothing.items():
                if val == value:
                    self._current = key

    def clear(self):
        self.fill(empty)
        self.blit(sprites.clothes.mannequin, (0, 0))

    def dress(self):
        self.clear()
        for item in self.clothing.values():
            self.blit(item, item.pos)
        self.parent.blit(self, self.pos)

class Clothing(pygame.Surface, ContainerMixin):
    def __init__(self, parent, pos, size):
        ContainerMixin.__init__(self, pos, size)
        pygame.Surface.__init__(self, size, flags=pygame.SRCALPHA)
        self.parent = parent
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
        self.fill(dye)
        self.parent.dress()


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

    def __init__(self, parent, image, pos):
        Button.__init__(self, image, pos)
        self.parent = parent

    @property
    def dye(self):
        return self.dyes[self.image]

    def on_click(self, pos):
        self.parent.parent.mannequin.current.dye(self.dye)
        print("reached")


class DyePanel(pygame.Surface, ContainerMixin):
    def __init__(self, parent, pos, size):
        ContainerMixin.__init__(self, pos, size)
        pygame.Surface.__init__(self, size, flags=pygame.SRCALPHA)
        self.parent = parent

        self.buttons = {
            "red": DyeButton(self, sprites.dyes.red, (0, 00)),
            "orange": DyeButton(self, sprites.dyes.orange, (0, 20)),
            "yellow": DyeButton(self, sprites.dyes.yellow, (0, 40)),
            "green": DyeButton(self, sprites.dyes.green, (0, 60)),
            "indigo": DyeButton(self, sprites.dyes.indigo, (0, 80)),
            "purple": DyeButton(self, sprites.dyes.purple, (0, 100)),
            "brown": DyeButton(self, sprites.dyes.brown, (0, 120)),
        }
        self.fill(empty)
        for button in self.buttons.values():
            self.blit(button, button.pos)

    def on_click(self, pos):
        for button in self.buttons.values():
            if pos in button:
                button.on_click(pos)