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

# Convert centroid values to influence maps
influence = {}
for culture in centroids:
    influence[culture] = make_influence_map(centroids[culture])

print(influence["greek"][centroids["greek"]])