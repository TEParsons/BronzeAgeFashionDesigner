import pygame


class Container:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @property
    def rect(self):
        return pygame.rect.Rect(*self.pos, *self.size)

    def __contains__(self, pos):
        assert isinstance(pos, (list, tuple)) and len(pos) == 2
        x, y = pos

        horiz = self.rect.left <= x <= self.rect.right
        vert = self.rect.top <= y <= self.rect.bottom

        return horiz and vert


class Button(Container):
    def __init__(self, surface, pos):
        Container.__init__(self, pos, surface.get_size())
        self.surface = surface

    def on_click(self, *args, **kwargs):
        return