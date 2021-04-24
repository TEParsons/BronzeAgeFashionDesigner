import numpy
from scipy.ndimage.filters import gaussian_filter

from .land import landmap

# Define centroid for each culture
centroids = {
    "italic": (22, 24),
    "greek": (31, 22),
    "thracean": (23, 15),
    "celtic": (12, 23),
    "iberian": (11, 38),
    "hittite": (35, 13),
    "egyptian": (46, 23),
    "berber": (22, 43),
    "lybian": (34, 37),
}


def make_influence_map(centroid):
    """Convert a centroid value to a cultural influence map"""
    # Start with map of 0s
    map = numpy.zeros(landmap.shape)
    # Set centroid to 255
    map[centroid] = 100
    # Blur
    map = gaussian_filter(map, 5)
    return map


def calculate_spread(culture):
    influence[culture]['outer'] = numpy.digitize(
        influence[culture]['inner'],
        [0.2, 0.3, 0.6]
    ) / 3


# Convert centroid values to influence maps
influence = {}
for culture in centroids:

    influence[culture] = {
        'inner': make_influence_map(centroids[culture])
    }
    calculate_spread(culture)


def advance_year():
    for culture in influence:
        xPlus = numpy.roll(influence[culture]['outer'], 1, 0)
        xMinus = numpy.roll(influence[culture]['outer'], -1, 0)
        yPlus = numpy.roll(influence[culture]['outer'], 1, 1)
        yMinus = numpy.roll(influence[culture]['outer'], -1, 1)
        influence[culture]['inner'] = (influence[culture]['inner'] + xPlus + xMinus + yPlus + yMinus) / 5
        calculate_spread(culture)