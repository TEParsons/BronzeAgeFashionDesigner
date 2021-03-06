import pygame
from bafd.scenes.map import spread
from bafd import sprites, utils, scenes, time


# Setup basic requirements
pygame.init()
clock = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 6)
# Setup window and virtual window
win = pygame.display.set_mode(utils.window.wsize)
vwin = utils.window.VirtualWindow(utils.window.vsize)
# Style window
pygame.display.set_caption('Bronze Age Fashion Designer')
pygame.display.set_icon(sprites.logo)
# Create map view
map_view = scenes.map.Map(utils.window.vsize)
# Create designer view
designer_view = scenes.designer.Designer(vwin)

vwin.scene = designer_view

t = 0
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Get key response
            done = event.key == pygame.K_ESCAPE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get mouse response
            if hasattr(vwin.scene, "on_click"):
                pos = utils.window.Position(*pygame.mouse.get_pos())
                vwin.scene.on_click(pos)
    # Update time
    clock.tick(60)
    t += clock.get_time() / 1000
    # Update year
    #map_view.year.check()
    # Flip screen
    vwin.scene.update()
    pygame.display.flip()