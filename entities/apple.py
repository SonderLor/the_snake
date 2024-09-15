from .game_object import GameObject
from random import randint
from constants import *
import pygame


class Apple(GameObject):

    def __init__(self):
        self.randomize_position()
        self.body_color = (255, 0, 0)
        super().__init__(self.position, self.body_color)

    def randomize_position(self):
        self.position = randint(0, 31), randint(0, 23)

    def draw(self):
        cords = self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE
        rect = pygame.Rect(cords, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        self.randomize_position()
