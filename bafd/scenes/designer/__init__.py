import pygame
from ... import sprites
from ...utils.ui import Button, ContainerMixin, Panel
from ...utils.colours import BaseColor, palette, empty


class Designer(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.blit(sprites.clothes.studio, (0, 0))

        # Make mannequin
        self.mannequin = Mannequin(self, (90, 5))
        self.mannequin.clothing['top'].set(sprites.clothes.chiton.both_high_short)
        self.mannequin.dress()

        # Make dye buttons
        dye_buttons = [
            DyeButton(self.mannequin, sprites.dyes.red, (1, 00)),
            DyeButton(self.mannequin, sprites.dyes.orange, (1, 20)),
            DyeButton(self.mannequin, sprites.dyes.yellow, (1, 40)),
            DyeButton(self.mannequin, sprites.dyes.green, (1, 60)),
            DyeButton(self.mannequin, sprites.dyes.indigo, (1, 80)),
            DyeButton(self.mannequin, sprites.dyes.purple, (1, 100)),
            DyeButton(self.mannequin, sprites.dyes.brown, (1, 120)),
            DyeButton(self.mannequin, sprites.dyes.none, (1, 140)),
        ]
        # Make dye panel and add buttons
        self.dye_panel = Panel(scene=self, pos=(5, 5), size=(20, 20 * len(dye_buttons)))
        for button in dye_buttons:
            self.dye_panel.children.append(button)
            self.dye_panel.blit(button, button.pos)
        self.blit(self.dye_panel, self.dye_panel.pos)

    def on_click(self, pos):
        if pos in self.dye_panel:
            self.dye_panel.on_click(pos)


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
        self.sprite = None
        self._dye = None

    def clear(self):
        self.fill(empty)

    def set(self, sprite):
        self.clear()
        self.sprite = sprite
        self.blit(sprite, (0, 0))
        self.dye(self._dye)

    def dye(self, dye):
        assert isinstance(dye, (BaseColor, type(None)))
        self._dye = dye
        self.sprite.dye(self._dye)
        self.clear()
        self.blit(self.sprite, (0, 0))
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
        sprites.dyes.none: None,
    }

    def __init__(self, mannequin, image, pos):
        Button.__init__(self, image, pos)
        self.mannequin = mannequin

    @property
    def dye(self):
        return self.dyes[self.image]

    def on_click(self, pos):
        self.mannequin.current.dye(self.dye)


class DyePanel(Panel):
    def __init__(self, parent, pos):
        self.parent = parent


    def on_click(self, pos):
        for button in self.buttons.values():
            if pos in button:
                button.on_click(pos)