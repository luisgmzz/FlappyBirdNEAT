from game.utils import load_image
from game.view.window import Window
from game.entities.bird import Bird
import pygame
import random

class Pipe:
    IMG = load_image("pipe.png")
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.IMG, False, True)
        self.PIPE_BOTTOM = self.IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height+self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win: Window):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

        # --- DEBUG: Dibuja rectángulos de las máscaras ---
        # Crear las máscaras

        # top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        # bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Conseguir los bounding rects
        # top_rect = top_mask.get_rect()
        # top_rect.x = self.x
        # top_rect.y = self.top

        # bottom_rect = bottom_mask.get_rect()
        # bottom_rect.x = self.x
        # bottom_rect.y = self.bottom

        # Dibujar los rectángulos
        # pygame.draw.rect(win.win, (0, 255, 0), top_rect, 2)  # Verde para el tubo de arriba
        # pygame.draw.rect(win.win, (0, 0, 255), bottom_rect, 2)  # Azul para el tubo de abajo

    def collide(self, bird: Bird):
        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (round(self.x - bird.get_x()), round(self.top - bird.get_y()))
        bottom_offset = (round(self.x - bird.get_x()), round(self.bottom - bird.get_y()))

        t_point = bird_mask.overlap(top_mask, top_offset)
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)

        return t_point or b_point
    
    def is_off_screen(self) -> bool:
        return self.x + self.PIPE_TOP.get_width() < 0

    # Checks if bird has passed this pipe for the first time 
    # and updates its internal state accordingly
    def has_passed(self, bird: Bird):
        if not self.passed and self.x < bird.get_x():
            self.passed = True
            return True
    
        return False
