import random

from src.constants import Thresholds, Grid
from src.objects import Wall, River, Food, Reward
from src.creatures import Prey, Predator
from src.helpers import random_position


class GameSeeder:
    def _prepare_objects(self):
        objects = []

        objects.extend(
            [Wall(position=[0, y], label=f'0,{y}') for y in range(0, Grid.SIZE)]
        )
        objects.extend(
            [Wall(position=[x, 0], label=f'{x},0') for x in range(0, Grid.SIZE)]
        )
        objects.extend(
            [
                Wall(position=[Grid.SIZE - 1, y], label=f'{Grid.SIZE - 1},{y}')
                for y in range(0, Grid.SIZE)
            ]
        )
        objects.extend(
            [
                Wall(position=[x, Grid.SIZE - 1], label=f'{x},{Grid.SIZE - 1}')
                for x in range(0, Grid.SIZE)
            ]
        )

        for i in range(Thresholds.INITIAL_RIVER):
            objects.append(River(position=random_position(), label=f'w{i}'))

        for i in range(Thresholds.INITIAL_FOOD):
            objects.append(Food(position=random_position(), label=f'@{i}'))

        for i in range(Thresholds.INITIAL_REWARD):
            objects.append(Reward(position=random_position(), label=f'${i}'))

        return objects

    def _prepare_creatures(self):
        creatures = []

        for i in range(Thresholds.INITIAL_PREY):
            creatures.append(Prey(position=random_position(), label=f'p{i}'))

        for i in range(Thresholds.INITIAL_PREDATOR):
            creatures.append(Predator(position=random_position(), label=f'P{i}'))

        return creatures

    def seed(self):
        objects = self._prepare_objects()
        creatures = self._prepare_creatures()

        return objects, creatures
