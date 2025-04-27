from game.entities.bird import Bird
from game.entities.pipe import Pipe
from game.entities.base import Base
from game.view.window import Window
import pygame

class Game:
    SPACE_BETWEEN_PIPES = 650
    FPS = 30

    def __init__(self):
        self.bird = Bird(230, 350)
        self.base = Base(730)
        self.pipes = [Pipe(self.SPACE_BETWEEN_PIPES)]
        self.window = Window(self)

        self.score = 0
        self.clock = pygame.time.Clock()

    def frame(self):
        add_pipe = False
        run = True

        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

        self.bird.move()
        self.base.move()

        rem = []
        for pipe in self.pipes:
            pipe.move()

            if pipe.is_off_screen():
                rem.append(pipe)

            if pipe.has_passed(self.bird):
                add_pipe = True


            if pipe.collide(self.bird):
                pass

        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(self.SPACE_BETWEEN_PIPES))

        for r in rem:
            self.pipes.remove(r)

        if self.bird.floor_hit():
            pass


        self.window.draw_window() 

        return run


    def run(self):
        while self.frame():
            pass


    def draw_bird(self):
        self.bird.draw(self.window)

    def draw_pipes(self):
        for pipe in self.pipes:
            pipe.draw(self.window)

    def draw_base(self):
        self.base.draw(self.window)

    def get_score(self):
        return self.score
