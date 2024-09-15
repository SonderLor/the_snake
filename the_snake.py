from entities import *
from constants import *
import pygame

from tests.conftest import snake, apple

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Функция обработки действий пользователя
def handle_keys(game_object):
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
    if cords1[0] == cords2[0] and cords1[1] == cords2[1]:
        return True
    return False


def main():
    # Инициализация PyGame:
    pygame.init()
    player_snake = Snake()
    current_apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(player_snake)
        player_snake.update_direction()
        player_snake.move()
        if is_cords_equal(player_snake.get_head_position(), current_apple.get_position()):
            player_snake.eat()
            current_apple.reset()
        player_snake.draw()
        current_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
