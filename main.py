from src.seeders import GameSeeder
from src.states import GameState
from src.game import Game


if __name__ == "__main__":
    objects, creatures = GameSeeder().seed()

    state = GameState(objects, creatures)

    game = Game(state)
    game.run()
