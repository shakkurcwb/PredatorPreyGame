import random

from src.constants import Thresholds, Color, Direction
from src.objects import Food, Reward
from src.helpers import random_position


class Creature:
    color = Color.BLUE

    def __init__(self, position=[0, 0], direction=Direction.UP, score=0, label="C"):
        self.position = position
        self.direction = direction
        self.score = score
        self.label = label

    # Think
    def _before_move(self, state):
        pass

    # Act
    def move(self, state):
        self._before_move(state)

        if self.direction == Direction.STOP:
            pass

        if self.direction == Direction.UP:
            self.position[1] -= 1

        if self.direction == Direction.RIGHT:
            self.position[0] += 1

        if self.direction == Direction.DOWN:
            self.position[1] += 1

        if self.direction == Direction.LEFT:
            self.position[0] -= 1

        self._after_move(state)

        return state

    # Learn
    def _after_move(self, state):
        pass

    #
    # Helpers
    #

    def _find_closest_creature(self, creatures: list):
        if not creatures:
            return None

        return min(creatures, key=lambda creature: abs(self.position[0] - creature.position[0]) + abs(self.position[1] - creature.position[1]))

    def _find_closest_object(self, objects: list):
        if not objects:
            return None

        return min(objects, key=lambda object: abs(self.position[0] - object.position[0]) + abs(self.position[1] - object.position[1]))

    def _move_towards_creature(self, creature):
        self.direction = (
            Direction.DOWN
            if self.position[1] < creature.position[1]
            else Direction.RIGHT
            if self.position[0] < creature.position[0]
            else Direction.UP
            if self.position[1] > creature.position[1]
            else Direction.LEFT
        )

    def _move_away_creature(self, creature):
        self.direction = (
            Direction.DOWN
            if self.position[1] > creature.position[1]
            else Direction.RIGHT
            if self.position[0] > creature.position[0]
            else Direction.UP
            if self.position[1] < creature.position[1]
            else Direction.LEFT
        )

    def _move_towards_object(self, object):
        self.direction = (
            Direction.DOWN
            if self.position[1] < object.position[1]
            else Direction.RIGHT
            if self.position[0] < object.position[0]
            else Direction.UP
            if self.position[1] > object.position[1]
            else Direction.LEFT
        )

    def _move_away_object(self, object):
        self.direction = (
            Direction.DOWN
            if self.position[1] > object.position[1]
            else Direction.RIGHT
            if self.position[0] > object.position[0]
            else Direction.UP
            if self.position[1] < object.position[1]
            else Direction.LEFT
        )

    def _get_distance_to_creature(self, creature):
        return abs(self.position[0] - creature.position[0]) + abs(self.position[1] - creature.position[1])

    def _get_distance_to_object(self, object):
        return abs(self.position[0] - object.position[0]) + abs(self.position[1] - object.position[1])


class Prey(Creature):
    color = Color.GREEN

    def _before_move(self, state):
        closest_food = self._find_closest_object(state.foods)
        closest_reward = self._find_closest_object(state.rewards)
        closest_predator = self._find_closest_creature(state.predators)

        # look for food
        self._move_towards_object(closest_food)

        # get reward when closer than food
        if self._get_distance_to_object(closest_reward) < self._get_distance_to_object(closest_food):
            self._move_towards_object(closest_reward)

        # run away from predator
        if self._get_distance_to_creature(closest_predator) < 4:
            # @todo: tricky to handle walls collisions when running away
            self._move_away_creature(closest_predator)

    def _after_move(self, state):
        closest_food = self._find_closest_object(state.foods)
        closest_reward = self._find_closest_object(state.rewards)
        closest_river = self._find_closest_object(state.rivers)
        closest_wall = self._find_closest_object(state.walls)

        # eat food
        if closest_food and self._get_distance_to_object(closest_food) < 1:
            state.remove_object(closest_food)
            self.score += closest_food.score

            # spawn new food
            food = Food(position=random_position(), label=f'f{len(state.foods)}')
            state.add_object(food)

            if self.score > Thresholds.COST_PREY_CLONE:
                self.score = self.score - Thresholds.COST_PREY_CLONE

                if Thresholds.MAX_PREY < len(state.preys):
                    # spawn a new prey
                    prey = Prey(position=random_position(), label=f'p{len(state.preys)}')
                    state.add_creature(prey)

        # get reward
        if closest_reward and self._get_distance_to_object(closest_reward) < 1:
            state.remove_object(closest_reward)
            self.score += closest_reward.score

            if Thresholds.MAX_REWARD > len(state.rewards):
                # spawn new reward
                reward = Reward(position=random_position(), label=f'r{len(state.rewards)}')
                state.add_object(reward)

            probability = random.randint(0, 4)
            if probability == 1: # 25% chance
                if Thresholds.MAX_REWARD > len(state.rewards):
                    # spawn new reward
                    reward = Reward(position=random_position(), label=f'r{len(state.rewards)}')
                    state.add_object(reward)
            elif probability == 2: # 25% chance
                if Thresholds.MAX_FOOD > len(state.foods):
                    # spawn new food
                    food = Food(position=random_position(), label=f'f{len(state.foods)}')
                    state.add_object(food)

            if self.score > Thresholds.COST_PREY_CLONE:
                # while enough score, spawn a new prey (in case of reward boost)
                clones = int(self.score // 10)
                if len(state.preys) + clones > Thresholds.MAX_PREY:
                    clones = Thresholds.MAX_PREY - len(state.preys)

                self.score = self.score - (10 * clones)

                for _ in range(clones):
                    # spawn a new prey
                    prey = Prey(position=random_position(), label=f'p{len(state.preys)}')
                    state.add_creature(prey)

        # punish when crossing river
        if closest_river and self._get_distance_to_object(closest_river) < 1:
            self.score += closest_river.score

        # punish when hitting wall
        if closest_wall and self._get_distance_to_object(closest_wall) < 1:
            self.score += closest_wall.score

            # reset position
            self.position = random_position()

            # decay color (highlight the cheater)
            r, g, b = self.color
            if g - 50 > 0:
                self.color = (r, g - 50, b)
            else:
                state.remove_creature(self)


class Predator(Creature):
    color = Color.RED

    def _before_move(self, state):
        closest_prey = self._find_closest_creature(state.preys)

        self._move_towards_creature(closest_prey)

    def _after_move(self, state):
        closest_prey = self._find_closest_creature(state.preys)
        closest_river = self._find_closest_object(state.rivers)

        # eat prey
        if closest_prey and self._get_distance_to_creature(closest_prey) < 1:
            state.remove_creature(closest_prey)
            self.score = self.score + Thresholds.PREY_SCORE

            if self.score > Thresholds.COST_PREDATOR_CLONE:
                self.score = self.score - Thresholds.COST_PREDATOR_CLONE

                if len(state.predators) < Thresholds.MAX_PREDATOR:
                    # spawn a new predator
                    predator = Predator(position=random_position(), label=f'p{len(state.predators)}')
                    state.add_creature(predator)

        # punish when crossing river
        if closest_river and self._get_distance_to_object(closest_river) < 1:
            self.score += closest_river.score
