import numpy
from scipy.ndimage.filters import gaussian_filter

from .map import landmap

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
cultures = list(centroids)

# Start with arrays of zeros for each culture
demographics = influence = numpy.array(
    numpy.zeros(landmap.shape),
    dtype=[(culture, float) for culture in cultures]
)

# Calculate starting demographics
for culture in cultures:
    # Set centroid to 255
    demographics[culture][centroids[culture]] = 255
    # Blur
    demographics[culture] = gaussian_filter(demographics[culture], 5)
