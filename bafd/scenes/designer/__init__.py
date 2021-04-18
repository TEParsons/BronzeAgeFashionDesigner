import pygame
from ... import sprites
from ...utils.ui import Button, ContainerMixin
from ...utils.colours import palette


class Designer(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)

        self.dyes = DyePanel((5, 5), (50, 150))
        self.blit(self.dyes, self.dyes.pos)

        self.mannequin = Mannequin((90, 5))
        self.blit(self.mannequin, self.mannequin.pos)

    def on_click(self, pos):
        if pos in self.dyes:
            self.dyes.on_click(pos)


class Mannequin(pygame.Surface, ContainerMixin):
    def __init__(self, pos):
        pygame.Surface.__init__(self, sprites.clothes.mannequin.get_size())
        self.pos = pos
        self.blit(sprites.clothes.mannequin, (0, 0))


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
        pygame.Surface.__init__(self, size)
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

        for button in self.buttons.values():
            self.blit(button, button.pos)

    def on_click(self, pos):
        for button in self.buttons.values():
            if pos in button:
                button.on_click(pos)