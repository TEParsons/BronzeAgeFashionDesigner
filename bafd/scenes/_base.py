import pygame
from bafd.utils.colours import empty
from bafd.utils.ui import ContainerMixin

class Scene(pygame.Surface):
    def __init__(self, win):
        pygame.Surface.__init__(self, win.get_size())
        self.win = win
        self.base = pygame.Surface(win.get_size())
        self.children = {}

    def clear(self):
        self.fill(empty)

    def reset(self):
        self.clear()
        self.blit(self.base, (0, 0))

    def update(self):
        self.reset()
        for child in self.children.values():
            # Update child if possible
            if hasattr(child, "update"):
                child.update()
            # Blit child at its position or (0, 0)
            if hasattr(child, "pos"):
                self.blit(child, child.pos)
            else:
                self.blit(child, (0, 0))
        self.win.blit(self, (0, 0))

    def on_click(self, pos):
        for child in self.children.values():
            if isinstance(child, ContainerMixin) and hasattr(child, "on_click"):
                if pos in child:
                    child.on_click(pos)