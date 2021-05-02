import pygame
from ...utils.colours import empty


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


class Panel(pygame.Surface, ContainerMixin):
    def __init__(self, scene, pos, size):
        ContainerMixin.__init__(self, pos, size)
        pygame.Surface.__init__(self, self.size, flags=pygame.SRCALPHA)
        self.fill(empty)
        self.scene = scene
        self.children = []

    def on_click(self, pos):
        # Convert from absolute position to relative
        pos = (pos[0] - self.pos[0], pos[1] - self.pos[1])
        # Call on_click method of any children clicked on
        for child in self.children:
            if pos in child and hasattr(child, "on_click"):
                child.on_click(pos)


class Button(pygame.Surface, ContainerMixin):
    def __init__(self, image, pos):
        ContainerMixin.__init__(self, pos, image.get_size())
        pygame.Surface.__init__(self, self.size, flags=pygame.SRCALPHA)
        self.image = image

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        assert isinstance(value, pygame.Surface)
        self.fill(empty)
        self._image = value
        self.blit(value, (0, 0))

    def on_click(self, pos):
        return