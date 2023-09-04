from src.objects import Wall, River, Food, Reward
from src.creatures import Prey, Predator

class GameState:
    is_running = False

    def __init__(self, objects: list = None, creatures: list = None):
        self.objects = objects if objects is not None else []
        self.creatures = creatures if creatures is not None else []

    def add_object(self, object):
        self.objects.append(object)

    def remove_object(self, object):
        self.objects.remove(object)

    def add_creature(self, creature):
        self.creatures.append(creature)

    def remove_creature(self, creature):
        self.creatures.remove(creature)

    @property
    def walls(self):
        return list(filter(lambda object: isinstance(object, Wall), self.objects))

    @property
    def rivers(self):
        return list(filter(lambda object: isinstance(object, River), self.objects))

    @property
    def foods(self):
        return list(filter(lambda object: isinstance(object, Food), self.objects))

    @property
    def rewards(self):
        return list(filter(lambda object: isinstance(object, Reward), self.objects))

    @property
    def preys(self):
        return list(filter(lambda creature: isinstance(creature, Prey), self.creatures))

    @property
    def predators(self):
        return list(filter(lambda creature: isinstance(creature, Predator), self.creatures))
