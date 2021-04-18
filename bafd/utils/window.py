import pygame
import screeninfo
from math import floor

vsize = (320, 180)

def calculate_scale():
    monitors = screeninfo.get_monitors()
    x = monitors[-1].width - 200
    y = monitors[-1].height - 200
    return min(
        floor(x / vsize[0]),
        floor(y / vsize[1])
    )

scale = calculate_scale()
wsize = tuple(d*scale for d in vsize)

class VirtualWindow(pygame.Surface):
    def __init__(self, *args, **kwargs):
        pygame.Surface.__init__(self, *args, **kwargs)
        self.win = pygame.display.get_surface()
        self._scene = None

    def blit(self, source, dest, area=None, special_flags=0):
        # Do usual blit
        pygame.Surface.blit(self, source, dest, area=area, special_flags=special_flags)
        # Resize to window
        buff = pygame.transform.scale(self, wsize)
        # Blit to render window
        self.win.blit(buff, (0, 0))

    @property
    def scene(self):
        return self._scene

    @scene.setter
    def scene(self, source):
        assert isinstance(source, pygame.Surface)

        self._scene = source
        self.blit(source, (0, 0))

class Position(tuple):
    def __new__(cls, x, y):
        vx = (vsize[0] / wsize[0]) * x
        vy = (vsize[1] / wsize[1]) * y
        return tuple.__new__(Position, (vx, vy))

    def __abs__(self):
        ax = (wsize[0] / vsize[0]) * self[0]
        ay = (wsize[1] / vsize[1]) * self[1]
        return (ax, ay)