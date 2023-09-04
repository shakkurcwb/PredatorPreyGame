class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    GREY = (128, 128, 128)
    AQUA = (0, 255, 255)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 165, 0)


class Screen:
    WIDTH = 800
    HEIGHT = 800

    FRAME_RATE = 10


class Grid:
    SIZE = 40
    CELL_SIZE = Screen.WIDTH // SIZE


class Thresholds:
    MAX_RIVER = 50
    MAX_FOOD = 10
    MAX_REWARD = 3
    MAX_PREY = 20
    MAX_PREDATOR = 10

    INITIAL_RIVER = 50
    INITIAL_FOOD = 5
    INITIAL_REWARD = 1
    INITIAL_PREY = 20
    INITIAL_PREDATOR = 2

    COST_PREY_CLONE = 10
    COST_PREDATOR_CLONE = 50
    PREY_SCORE = 10


class Direction:
    STOP = -1
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
