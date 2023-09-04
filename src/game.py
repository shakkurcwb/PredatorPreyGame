import pygame

from src.constants import Screen, Color, Grid

class Game:
    GAME_TITLE = "Predator vs Prey Game"

    def __init__(self, state):
        self.state = state

        # Initialize pygame
        pygame.init()

    def run(self):
        # Initialize the screen
        self.screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))

        # Set the title
        pygame.display.set_caption(self.GAME_TITLE)

        # Initialize the clock
        clock = pygame.time.Clock()

        self.state.running = True
        while self.state.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state.running = False

            self._update()

            # Update the display
            pygame.display.flip()

            # Adjust the frame rate
            clock.tick(Screen.FRAME_RATE)

        pygame.quit()

    def _update(self):
        # Clear the screen
        self.screen.fill(Color.WHITE)

        # Draw the grid
        self._draw_grid()

        # Draw the objects
        for object in self.state.objects:
            self._draw_object(object)

            # print('object', object.__class__.__name__, object.label, object.position)

        # Move creatures then draw them
        for creature in self.state.creatures:
            creature.move(self.state)
            self._draw_creature(creature)

            print('creature', creature.__class__.__name__, creature.label, creature.position, creature.score)

        # Check if the game is over
        if not self.state.preys:
            print('Game-Over')
            self.state.running = False

    def _draw_grid(self):
        for i in range(Grid.SIZE):
            pygame.draw.line(self.screen, Color.BLACK, (i * Grid.CELL_SIZE, 0), (i * Grid.CELL_SIZE, Screen.HEIGHT))
            pygame.draw.line(self.screen, Color.BLACK, (0, i * Grid.CELL_SIZE), (Screen.WIDTH, i * Grid.CELL_SIZE))

    def _draw_creature(self, creature):
        # Draw the creature
        pygame.draw.circle(self.screen, creature.color, (creature.position[0] * Grid.CELL_SIZE + Grid.CELL_SIZE // 2, creature.position[1] * Grid.CELL_SIZE + Grid.CELL_SIZE // 2), Grid.CELL_SIZE // 2)

        # Draw the label
        font = pygame.font.Font(None, 12)
        label_text = font.render(creature.label, True, (0, 0, 0))
        label_position = (creature.position[0] * Grid.CELL_SIZE + Grid.CELL_SIZE // 4, creature.position[1] * Grid.CELL_SIZE + Grid.CELL_SIZE // 4)
        self.screen.blit(label_text, label_position)

    def _draw_object(self, object):
        # Draw the object
        pygame.draw.rect(self.screen, object.color, (object.position[0] * Grid.CELL_SIZE, object.position[1] * Grid.CELL_SIZE, Grid.CELL_SIZE, Grid.CELL_SIZE))

        # Draw the label
        font = pygame.font.Font(None, 12)
        label_text = font.render(object.label, True, (0, 0, 0))
        label_position = (object.position[0] * Grid.CELL_SIZE + Grid.CELL_SIZE // 4, object.position[1] * Grid.CELL_SIZE + Grid.CELL_SIZE // 4)
        self.screen.blit(label_text, label_position)
