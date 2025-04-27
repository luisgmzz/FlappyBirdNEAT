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

    def draw(self, win: Window or pygame.Surface):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird: Bird):
        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return (t_point or b_point)
    
    def is_off_screen(self) -> bool:
        return self.x + self.PIPE_TOP.get_width() < 0

    # Checks if bird has passed this pipe for the first time 
    # and updates its internal state accordingly
    def has_passed(self, bird: Bird):
        if not self.passed and self.x < bird.get_x():
            self.passed = True
            return True
    
        return False
