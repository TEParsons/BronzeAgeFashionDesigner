import pygame
from pathlib import Path
import numpy


def get_dye_spec(path):
    assert isinstance(path, (str, Path))
    path = Path(path)
    assert path.is_file()
    # Get dyable region
    rpath = path.parent / (path.stem + "_.png")
    region = pygame.image.load(str(rpath))
    region_arr = pygame.surfarray.array2d(region) != 255
    # Get luminance map
    lum_array = pygame.surfarray.array2d(region)
    surface = pygame.image.load(str(rpath))
    w, h = lum_array.shape
    for x in range(w):
        for y in range(h):
            # Skip if not in region
            if not region_arr[x, y]:
                lum_array[x, y] = 99
                continue
            lum_array[x, y] = numpy.round(
                surface.get_at((x, y))[0] / 16
            ) - 8
    # Save luminance array
    new_file = path.parent / (path.stem + ".csv")
    numpy.savetxt(new_file, lum_array, fmt="%5i")

get_dye_spec("F:\\GitHub\\BronzeAgeFashionDesigner\\bafd\\sprites\\clothes\\alopekis\\long.png")
get_dye_spec("F:\\GitHub\\BronzeAgeFashionDesigner\\bafd\\sprites\\clothes\\alopekis\\short.png")
