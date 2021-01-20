import numpy as np
from itertools import islice
from random import randint

def set_initial_agressiveness(nation):
    return np.random.rand()

def set_initial_wealth(agent):
    return np.random.randint(0,100)

def set_initial_reputation(agent):
    return np.random.randint(0,100)

def make_random_chunks(li, min_chunk=1, max_chunk=3):
    it = iter(li)
    while True:
        nxt = list(islice(it,randint(min_chunk,max_chunk)))
        if nxt:
            yield nxt
        else:
            break

def get_color(i):
    """
    given an int returns 'random' color
    """
    # Implement later: agression color
    n = 7
    i = (i % n)
    if i == 0:
        return 'blue'
    if i == 1:
        return 'green'
    if i == 2:
        return 'red'
    if i == 3:
        return 'cyan'
    if i == 4:
        return 'magenta'
    if i == 5:
        return 'yellow'
    if i == 6:
        return  'black'
