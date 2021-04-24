import pygame

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
main_map = scenes.map.Map(utils.window.vsize)
# Create designer view
designer_view = scenes.designer.Designer(utils.window.vsize)

vwin.scene = main_map

year = time.Year(-1500, length=0.1)
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
    year.check()
    # Flip screen
    main_map.update_overlay()
    vwin.blit(vwin.scene, (0, 0))
    pygame.display.flip()