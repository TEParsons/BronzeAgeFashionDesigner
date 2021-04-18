import pygame

from bafd import sprites, utils, scenes

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
main_map = scenes.map.Map(utils.window.vsize)
# Create designer view
designer_view = scenes.designer.Designer(utils.window.vsize)

vwin.scene = designer_view

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            done = event.key == pygame.K_ESCAPE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if hasattr(vwin.scene, "on_click"):
                pos = utils.window.Position(*pygame.mouse.get_pos())
                vwin.scene.on_click(pos)
    clock.tick(60)
    pygame.display.flip()