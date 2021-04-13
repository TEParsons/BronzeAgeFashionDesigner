import pygame
from packaging.version import Version

from bafd import sprites, utils
from bafd.scenes import map

# Mark version number
__version__ = Version("0.0.0")

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

main_map = map.Map(vwin)


pygame.time.wait(2000)
# # Pass 10 years
# year = 0
# while year <= 10:
#     pygame.time.wait(1000)
#     map.appeal.player['greek'] += 20
#     map.appeal.calculate_appeal(map.appeal.player)
#     for culture in map.influence.influence:
#         map.influence.influence[culture] += map.appeal.appeal["player"][culture]
#     main_map.update_overlay()
#     year += 1


