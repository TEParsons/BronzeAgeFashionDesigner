import pygame


class ContainerMixin:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    @property
    def rect(self):
        return pygame.rect.Rect(*self.pos, *self.size)

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def w(self):
        return self.size[0]

    @property
    def h(self):
        return self.size[1]

    def __contains__(self, pos):
        assert isinstance(pos, (list, tuple)) and len(pos) == 2
        x, y = pos

        horiz = self.rect.left <= x <= self.rect.right
        vert = self.rect.top <= y <= self.rect.bottom

        return horiz and vert


class Button(pygame.Surface, ContainerMixin):
    def __init__(self, image, pos):
        pygame.Surface.__init__(self, image.get_size())
        self.pos = pos
        self.size = image.get_size()
        self.image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        assert isinstance(value, pygame.Surface)
        self._image = value
        self.blit(value, (0, 0))

    def on_click(self, *args, **kwargs):
        return