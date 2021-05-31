import json

import pygame
from ... import sprites
from .._base import Scene
from ...utils.ui import Button, ContainerMixin, Panel
from ...utils.colours import BaseColor, palette, empty


class Designer(Scene):
    def __init__(self, win):
        Scene.__init__(self, win)
        # Set background
        self.base = sprites.clothes.studio

        # Make mannequin
        self.children['mannequin'] = self.mannequin = Mannequin(scene=self, pos=(90, 5))
        self.mannequin.clothing = {
            'top': ClothingItem(scene=self, parent=self.mannequin,
                                sprite=sprites.clothes.chiton,
                                pos=(0, 60), size=(self.mannequin.w, self.mannequin.h-70)),
            'hat': ClothingItem(scene=self, parent=self.mannequin,
                                sprite=sprites.clothes.alopekis,
                                pos=(0, 0), size=(self.mannequin.w, 80))
        }
        self.mannequin.current = 'hat'

        # Make dye buttons
        self.children['dyes'] = self.dye_panel = Panel(scene=self, pos=(5, 5), size=(20, 20*8))
        self.dye_panel.children = [
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.red, pos=(1, 00)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.orange, pos=(1, 20)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.yellow, pos=(1, 40)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.green, pos=(1, 60)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.indigo, pos=(1, 80)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.purple, pos=(1, 100)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.brown, pos=(1, 120)),
            DyeButton(scene=self, parent=self.dye_panel, image=sprites.dyes.none, pos=(1, 140)),
        ]

        # Make style ctrls
        self.children['style'] = self.style_ctrls = Panel(scene=self, pos=(150, 90), size=(27*2, 27))
        self.style_ctrls.children = [
            StyleButton(scene=self, parent=self.style_ctrls, image=sprites.ui.left, pos=(1, 1), func="prev"),
            StyleButton(scene=self, parent=self.style_ctrls, image=sprites.ui.right, pos=(26, 1), func="next"),
        ]

    @property
    def json(self):
        return {
            'mannequin': self.mannequin.json
        }

    @json.setter
    def json(self, value):
        assert isinstance(value, dict)
        # Load to mannequin
        self.mannequin.json = value['mannequin']


class Mannequin(pygame.Surface, ContainerMixin):
    def __init__(self, scene, pos):
        ContainerMixin.__init__(self, pos, sprites.clothes.mannequin.get_size())
        pygame.Surface.__init__(self, self.size, flags=pygame.SRCALPHA)
        self.scene = scene
        self.clothing = {}
        self._current = None

    @property
    def current(self):
        if self._current in self.clothing:
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

    def reset(self):
        self.clear()
        self.blit(sprites.clothes.mannequin, (0, 0))

    def update(self):
        self.reset()
        for item in self.clothing.values():
            item.update()
            self.blit(item, item.pos)

    @property
    def json(self):
        return {
            key: value.json
            for key, value in self.clothing.items()
        }

    @json.setter
    def json(self, value):
        assert isinstance(value, dict)
        # Load each item
        for key, value in value.items():
            self.clothing[key].json = value


class ClothingItem(pygame.Surface, ContainerMixin):
    def __init__(self, scene, parent, sprite, pos, size):
        ContainerMixin.__init__(self, pos, size)
        pygame.Surface.__init__(self, size, flags=pygame.SRCALPHA)
        self.scene = scene
        self.parent = parent
        self.sprite = sprite
        self._dye = None
        self._style = self.sprite.styles[0]

    def clear(self):
        self.fill(empty)

    def update(self):
        self.clear()
        self.sprite.update()
        self.blit(self.sprite, (0, 0))

    def set(self, sprite):
        self.clear()
        self.sprite = sprite
        self.blit(sprite, (0, 0))
        self.dye(self._dye)

    def dye(self, dye):
        assert isinstance(dye, (BaseColor, type(None)))
        self._dye = dye
        self.sprite.dye = self._dye

    def next(self):
        self.sprite.next()

    def prev(self):
        self.sprite.prev()

    @property
    def json(self):
        return {
            'name': self.sprite.path.stem,
            'dye': self._dye,
            'style': self.sprite.style
        }

    @json.setter
    def json(self, value):
        assert isinstance(value, dict)
        # Load base sprite
        self.sprite = getattr(sprites.clothes, value['name'])
        # Load dye
        dye = BaseColor("white")
        dye.hex = value['dye']
        self.dye(dye)
        # Load style
        self.sprite.style = value['style']

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

    def __init__(self, scene, parent, image, pos):
        Button.__init__(self, image, pos)
        self.scene = scene
        self.parent = parent

    @property
    def dye(self):
        return self.dyes[self.image]

    def on_click(self, pos):
        self.scene.mannequin.current.dye(self.dye)


class StyleButton(Button):
    def __init__(self, scene, parent, image, pos, func):
        Button.__init__(self, image, pos)
        self.scene = scene
        self.parent = parent
        self.func = func

    def on_click(self, pos):
        func = getattr(self.scene.mannequin.current, self.func)
        func()