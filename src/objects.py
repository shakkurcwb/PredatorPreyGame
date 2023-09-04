from src.constants import Color


class Object:
    color = Color.YELLOW
    is_walkable = False
    is_permanent = False
    score = 0

    def __init__(self, position=[0, 0], label="O"):
        self.position = position
        self.label = label


class Wall(Object):
    color = Color.GREY
    is_walkable = False
    is_permanent = True
    score = -100


class River(Object):
    color = Color.AQUA
    is_walkable = True
    is_permanent = False
    score = -10


class Food(Object):
    color = Color.PURPLE
    is_walkable = False
    is_permanent = False
    score = 5


class Reward(Object):
    color = Color.ORANGE
    is_walkable = False
    is_permanent = False
    score = 50
