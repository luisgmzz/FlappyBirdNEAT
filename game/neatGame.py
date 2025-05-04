import pygame.display
import neat

from game.entities.base import Base
from game.entities.bird import Bird
from game.entities.pipe import Pipe
from game.game import Game
from game.view.neatWindow import NeatWindow

pygame.font.init()

class NeatGame:
    FPS = 120

    def __init__(self, genomes, config, gen):
        self.genomes = genomes
        self.config = config

        self.score = 0
        self.gen = gen
        self.birds: list[Bird] = []
        self.nets = []
        self.ge = []

        self.pipes: list[Pipe] = [Pipe(Game.SPACE_BETWEEN_PIPES)]
        self.base = Base(730)
        self.clock = pygame.time.Clock()

        self.window = NeatWindow(self)

        for _, g in self.genomes:
            net = neat.nn.FeedForwardNetwork.create(g, self.config)
            self.nets.append(net)
            self.birds.append(Bird(230, 350))

            g.fitness = 0

            self.ge.append(g)

    def run_frame(self):
        add_pipe = False

        self.clock.tick(self.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pipe_ind = 0
        if len(self.birds) > 0:
            if len(self.pipes) > 1 and self.birds[0].get_x() > self.pipes[0].get_x() + self.pipes[0].get_top_pipe().get_width():
                pipe_ind = 1
        else:
            return

        for bird in self.birds:
            i = self.birds.index(bird)
            bird.move()
            self.ge[i].fitness += .1

            output = self.nets[i].activate(
                (bird.get_y(), abs(bird.get_y() - self.pipes[pipe_ind].get_height()), abs(bird.get_y() - self.pipes[pipe_ind].get_bottom())))
            if output[0] > .5:
                bird.jump()

        self.base.move()

        rem = []
        for pipe in self.pipes:
            pipe.move()

            if pipe.is_off_screen():
                rem.append(pipe)

            for bird in self.birds:
                if pipe.collide(bird):
                    i = self.birds.index(bird)
                    self.ge[i].fitness -= 1  # Penalize if the bird collides
                    self.birds.pop(i)
                    self.nets.pop(i)
                    self.ge.pop(i)

                if pipe.has_passed(bird):
                    add_pipe = True

        if add_pipe:
            self.score += 1
            for g in self.ge:
                g.fitness += 5

            self.pipes.append(Pipe(Game.SPACE_BETWEEN_PIPES))

        for r in rem:
            self.pipes.remove(r)

        for bird in self.birds:
            if bird.floor_hit() or bird.touched_sky():
                i = self.birds.index(bird)
                self.birds.pop(i)
                self.nets.pop(i)
                self.ge.pop(i)

        self.window.draw_window()

    def run_generation(self):
        self.score = 0
        while len(self.birds) > 0 and self.score < 30:
            self.run_frame()


GEN = 1

def run_neat(genomes, config):
    global GEN
    game = NeatGame(genomes, config, GEN)
    game.run_generation()
    GEN += 1