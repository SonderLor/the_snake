import pygame
from random import choice

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 33, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
ROCK_COLOR = (128, 128, 128)
POISON_COLOR = (0, 0, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SPEED = 10
SPEED_INCREMENT = 1
MIN_SPEED = 5
MAX_SPEED = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

ALL_CELLS = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))

HIGH_SCORE_FILE = "high_score.txt"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def get_position(self):
        return self.position

    def draw_square(self, position, color, border_color=BORDER_COLOR):
        cords = position[0] * GRID_SIZE, position[1] * GRID_SIZE
        rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 2)

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = (0, 0)
        super().__init__(self.position, self.body_color)

    def randomize_position(self, snake_positions):
        occupied_cells = set(snake_positions)
        free_cells = ALL_CELLS - occupied_cells
        self.position = choice(tuple(free_cells))

    def draw(self):
        self.draw_square(self.position, self.body_color)

    def erase(self, color):
        self.draw_square(self.position, color)

    def reset(self, snake_positions):
        self.randomize_position(snake_positions)


class Rock(GameObject):
    def __init__(self):
        self.body_color = ROCK_COLOR
        self.position = (0, 0)
        super().__init__(self.position, self.body_color)

    def randomize_position(self, snake_positions):
        occupied_cells = set(snake_positions)
        free_cells = ALL_CELLS - occupied_cells
        self.position = choice(tuple(free_cells))

    def draw(self):
        self.draw_square(self.position, self.body_color)

    def reset(self, snake_positions):
        self.randomize_position(snake_positions)


class Poison(GameObject):
    def __init__(self):
        self.body_color = POISON_COLOR
        self.position = (0, 0)
        super().__init__(self.position, self.body_color)

    def randomize_position(self, snake_positions):
        occupied_cells = set(snake_positions)
        free_cells = ALL_CELLS - occupied_cells
        self.position = choice(tuple(free_cells))

    def draw(self):
        self.draw_square(self.position, self.body_color)

    def reset(self, snake_positions):
        self.randomize_position(snake_positions)


class Snake(GameObject):
    def __init__(self):
        self.length = None
        self.next_direction = None
        self.direction = None
        self.positions = None
        self.last = None
        self.body_color = SNAKE_COLOR
        self.reset()
        super().__init__(self.positions[0], self.body_color)

    def get_head_position(self):
        return self.positions[0]

    def get_positions(self):
        return self.positions

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head = self.get_head_position()
        next_cell = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        if next_cell in self.positions:
            self.die()
            self.reset()
        else:
            self.positions.insert(0, next_cell)
            self.last = self.positions.pop()

    def draw(self):
        self.draw_square(self.get_head_position(), self.body_color)

        if self.last:
            self.draw_square(self.last, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)

    def die(self):
        for position in self.positions:
            self.draw_square(position, BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def eat(self):
        head = self.get_head_position()
        next_cell = head[0] + self.direction[0], head[1] + self.direction[1]
        self.positions.insert(0, next_cell)

    def shrink(self):
        if len(self.positions) > 1:
            self.draw_square(self.positions.pop(), BOARD_BACKGROUND_COLOR, BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    direction_opposites = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }

    key_to_direction = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT
    }

    global SPEED
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            new_direction = key_to_direction.get(event.key)
            if new_direction and new_direction != direction_opposites.get(game_object.direction):
                game_object.next_direction = new_direction
            elif event.key == pygame.K_q and SPEED > MIN_SPEED:
                SPEED -= SPEED_INCREMENT
            elif event.key == pygame.K_w and SPEED < MAX_SPEED:
                SPEED += SPEED_INCREMENT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def is_cords_equal(cords1, cords2):
    return cords1[0] == cords2[0] and cords1[1] == cords2[1]


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 1


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


def main():
    pygame.init()
    player_snake = Snake()
    apples = [Apple() for _ in range(3)]
    rocks = [Rock() for _ in range(3)]
    poisons = [Poison() for _ in range(3)]
    high_score = load_high_score()

    for apple in apples:
        apple.reset(player_snake.get_positions())
    for rock in rocks:
        rock.reset(player_snake.get_positions())
    for poison in poisons:
        poison.reset(player_snake.get_positions())

    while True:
        clock.tick(SPEED)
        handle_keys(player_snake)
        player_snake.update_direction()
        player_snake.move()

        for apple in apples:
            if is_cords_equal(player_snake.get_head_position(), apple.get_position()):
                apple.erase(SNAKE_COLOR)
                player_snake.eat()
                apple.reset(player_snake.get_positions())

        for rock in rocks:
            if is_cords_equal(player_snake.get_head_position(), rock.get_position()):
                player_snake.die()
                player_snake.reset()

        for poison in poisons:
            if is_cords_equal(player_snake.get_head_position(), poison.get_position()):
                player_snake.shrink()
                poison.reset(player_snake.get_positions())

        current_score = len(player_snake.get_positions())
        if current_score > high_score:
            high_score = current_score
            save_high_score(high_score)

        pygame.display.set_caption(
            f'Змейка - Рекорд: {high_score} - '
            f'Скорость: {SPEED} - q: уменьшить, w: увеличить'
        )

        player_snake.draw()
        for apple in apples:
            apple.draw()
        for rock in rocks:
            rock.draw()
        for poison in poisons:
            poison.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
