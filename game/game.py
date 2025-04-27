import time

from game.entities.bird import Bird
from game.entities.pipe import Pipe
from game.entities.base import Base
from game.view.window import Window
import pygame

class Game:
    SPACE_BETWEEN_PIPES = 650
    FPS = 30

    def __init__(self, net=None):
        self.bird = Bird(230, 350)
        self.base = Base(730)
        self.pipes = [Pipe(self.SPACE_BETWEEN_PIPES)]
        self.window = Window(self)

        self.score = 0
        self.clock = pygame.time.Clock()

        if net:
            self.ai_playing = True
            self.net = net
        else:
            self.ai_playing = False
        self.keepRunning = True

    def frame(self):
        add_pipe = False

        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Cerrado")
                self.keepRunning = False

            if not self.ai_playing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

        self.bird.move()
        if self.ai_playing:
            pipe_ind = 0
            if len(self.pipes) > 1 and self.bird.get_x() > self.pipes[0].get_x() + self.pipes[0].get_top_pipe().get_width():
                pipe_ind = 1

            output = self.net.activate(
                (self.bird.get_y(), abs(self.bird.get_y() - self.pipes[pipe_ind].get_height()), abs(self.bird.get_y() - self.pipes[pipe_ind].get_bottom())))
            if output[0] > .5:
                self.bird.jump()

        self.base.move()

        rem = []
        for pipe in self.pipes:
            pipe.move()

            if pipe.is_off_screen():
                rem.append(pipe)

            if pipe.has_passed(self.bird):
                add_pipe = True


            if pipe.collide(self.bird):
                print("Chocado")
                self.keepRunning = False

        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(self.SPACE_BETWEEN_PIPES))

        for r in rem:
            self.pipes.remove(r)

        if self.bird.floor_hit() or self.bird.touched_sky():
            print("perdiste")
            self.keepRunning = False


        self.window.draw_window()


    def run(self):
        while self.keepRunning:
            self.frame()


    def draw_bird(self):
        self.bird.draw(self.window)

    def draw_pipes(self):
        for pipe in self.pipes:
            pipe.draw(self.window)

    def draw_base(self):
        self.base.draw(self.window)

    def get_score(self):
        return self.score
