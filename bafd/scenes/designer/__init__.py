import pygame
from ... import sprites
from ...utils.ui import Button, ContainerMixin
from ...utils.colours import palette


class Designer(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)

        self.dyes = DyePanel((2, 2), (50, 150))
        self.blit(self.dyes.surface, self.dyes.pos)

    def on_click(self, pos):
        if pos in self.dyes:
            self.dyes.on_click(pos)


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

        self.red = DyeButton(sprites.dyes.red, (10, 10))
        self.orange = DyeButton(sprites.dyes.orange, (10, 30))
        self.yellow = DyeButton(sprites.dyes.yellow, (10, 50))
        self.green = DyeButton(sprites.dyes.green, (10, 70))
        self.indigo = DyeButton(sprites.dyes.indigo, (10, 90))
        self.purple = DyeButton(sprites.dyes.purple, (10, 110))
        self.brown = DyeButton(sprites.dyes.brown, (10, 130))

        self.buttons = [self.red, self.orange, self.yellow, self.green, self.indigo, self.purple, self.brown]
        for button in self.buttons:
            self.surface.blit(button.surface, button.pos)

    def on_click(self, pos):
        for button in self.buttons:
            if pos in button:
                button.on_click(pos)