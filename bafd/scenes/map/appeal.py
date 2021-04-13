import numpy
from scipy.ndimage.filters import gaussian_filter

from .land import landmap
from .influence import influence

player = {
    "italic": 100,
    "greek": 0,
    "thracean": 0,
    "celtic": 0,
    "iberian": 0,
    "hittite": 0,
    "egyptian": 0,
    "berber": 0,
    "lybian": 0,
}
npc1 = {
    "italic": 0,
    "greek": 0,
    "thracean": 0,
    "celtic": 0,
    "iberian": 0,
    "hittite": 0,
    "egyptian": 0,
    "berber": 0,
    "lybian": 100,
}

appeal = {
    "player": {},
    "npc1": {},
}

def calculate_appeal(player):
    buff = {}
    proportion = {culture: val / sum(player.values()) for culture, val in player.items()}
    for culture in influence:
        buff[culture] = influence[culture].copy()
        buff[culture] *= proportion[culture]
    appeal["player"] = buff

calculate_appeal(player)
