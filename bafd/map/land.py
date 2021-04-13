import numpy
from pathlib import Path

__folder__ = Path(__file__).parent

# Read csv of land/water tiles
landmap = numpy.fliplr(
    numpy.genfromtxt(__folder__ / 'land.csv', delimiter=',')
)