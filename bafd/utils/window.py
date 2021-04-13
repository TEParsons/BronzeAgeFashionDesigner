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

    def blit(self, source, dest, area=None, special_flags=0):
        # Do usual blit
        pygame.Surface.blit(self, source, dest, area=area, special_flags=special_flags)
        # Resize to window
        buff = pygame.transform.scale(self, wsize)
        # Blit to render window
        self.win.blit(buff, (0, 0))
