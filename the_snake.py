import pygame
from random import randint

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Скорость движения змейки:
SPEED = 10

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для объектов игры."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        self.position = position
        self.body_color = body_color

    def get_position(self):
        """Возвращает текущую позицию объекта."""
        return self.position

    def draw(self):
        """Рисует объект на экране."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self):
        self.randomize_position()
        self.body_color = APPLE_COLOR
        super().__init__(self.position, self.body_color)

    def randomize_position(self):
        """Генерирует случайную позицию для яблока."""
        self.position = randint(0, 31), randint(0, 23)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        cords = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает положение яблока."""
        self.randomize_position()


class Snake(GameObject):
    """Класс, представляющий змейку."""

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
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в направлении движения."""
        head = self.get_head_position()
        next_cell = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        if next_cell in self.positions:
            self.reset()
        else:
            self.positions.insert(0, next_cell)
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            cords = position[0] * GRID_SIZE, position[1] * GRID_SIZE
            rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            cords = self.last[0] * GRID_SIZE, self.last[1] * GRID_SIZE
            last_rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def eat(self):
        """Добавляет сегмент к змейке."""
        head = self.get_head_position()
        next_cell = head[0] + self.direction[0], head[1] + self.direction[1]
        self.positions.insert(0, next_cell)


def handle_keys(game_object):
    """Обрабатывает действия пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def is_cords_equal(cords1, cords2):
    """Сравнивает две координаты."""
    return cords1[0] == cords2[0] and cords1[1] == cords2[1]


def main():
    """Запускает главный цикл игры."""
    pygame.init()
    player_snake = Snake()
    current_apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(player_snake)
        player_snake.update_direction()
        player_snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)

        if is_cords_equal(
                player_snake.get_head_position(), current_apple.get_position()
        ):
            player_snake.eat()
            current_apple.reset()

        player_snake.draw()
        current_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
