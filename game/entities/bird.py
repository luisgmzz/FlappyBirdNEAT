from game.utils import load_image, rotate_image 
from game.view.window import Window
import pygame

class Bird:
    IMGS = [
        load_image("bird1.png"),
        load_image("bird2.png"),
        load_image("bird3.png"),
    ]
    MAX_ROTATION = 25
    MIN_ROTATION = -90
    ROT_VEL = 20
    ANIMATION_TIME = 5
    MAX_VEL = 16

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0 # ticks from last jump
        self.height = self.y # y position of the last jump
        self.vel = 0
        self.img_count = 0 # ticks from the begin of last cycle of images
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self): # each tick
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 

        if d >= self.MAX_VEL:
            d = self.MAX_VEL

        if d < 0: # a bit more upwards momentum
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height+50: # moving upwards or being above our last jump position 
            if self.tilt < self.MAX_ROTATION: # TODO check este if probalmemente sobra
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > self.MIN_ROTATION:
                self.tilt -= self.ROT_VEL
            

    def draw(self, win: Window):
        self.img_count += 1

        # each 5 frames, change img
        # TODO mejorar
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= self.MIN_ROTATION + 10: # if falling, dont flap the wings
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image, rect = rotate_image(self.img, self.tilt, self.x, self.y)

        win.blit(rotated_image, rect.center)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
    def get_x(self) -> int:
        return self.x
    
    def floor_hit(self) -> bool:
        return self.x + self.img.get_height() >= 730