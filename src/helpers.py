import random

from src.constants import Grid


def random_position():
    return [random.randint(1, Grid.SIZE - 2), random.randint(1, Grid.SIZE - 2)]
