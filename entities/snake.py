from .game_object import GameObject
from constants import *


class Snake(GameObject):
    def __init__(self):
        self.length = None
        self.next_direction = None
        self.direction = None
        self.positions = None
        self.last = None
        self.body_color = (0, 255, 0)
        self.reset()
        super().__init__(self.positions[0], self.body_color)

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.get_head_position()
        next_cell = (head[0] + self.direction[0]) % GRID_WIDTH, (head[1] + self.direction[1]) % GRID_HEIGHT
        if next_cell in self.positions:
            self.reset()
        else:
            self.positions.insert(0, next_cell)
            self.last = self.positions.pop()

    def draw(self):
        for position in self.positions:
            cords = position[0] * GRID_SIZE, position[1] * GRID_SIZE
            rect = (pygame.Rect(cords, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Затирание последнего сегмента
        if self.last:
            cords = self.last[0] * GRID_SIZE, self.last[1] * GRID_SIZE
            last_rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        if self.positions:
            for position in self.positions:
                cords = position[0] * GRID_SIZE, position[1] * GRID_SIZE
                dead_rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, dead_rect)
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def eat(self):
        head = self.get_head_position()
        next_cell = head[0] + self.direction[0], head[1] + self.direction[1]
        self.positions.insert(0, next_cell)
