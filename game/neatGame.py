import pygame.display
import neat

from game.entities.base import Base
from game.entities.bird import Bird
from game.entities.pipe import Pipe
from game.game import Game
from game.view.window import Window

pygame.font.init()

class NeatGame:
    GEN = 0
    def draw_window(self, win: pygame.Surface, birds: list[Bird], pipes: list[Pipe], base: Base, score: int, gen: int):
        score_text = Window.STAT_FONT.render("Score: " + str(score), 1, Window.COLOR_WHITE)
        gen_text = Window.STAT_FONT.render("Gen: " + str(gen), 1, Window.COLOR_WHITE)

        if gen == 0:
            gen = 1

        win.blit(Window.BG_IMG, (0, 0))


        for pipe in pipes:
            pipe.draw(win)

        base.draw(win)

        for bird in birds:
            bird.draw(win)


        win.blit(score_text, (Window.WIDTH-10-score_text.get_width(), 10))
        win.blit(gen_text, (10, 10))
        pygame.display.update()

    def run_neat(self, genomes, config):
        self.GEN += 1
        nets = []
        ge = []
        birds: list[Bird] = []

        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            birds.append(Bird(230, 350))
            g.fitness = 0
            ge.append(g)

        base = Base(730)
        pipes = [Pipe(Game.SPACE_BETWEEN_PIPES)]

        win = pygame.display.set_mode((Window.WIDTH, Window.HEIGHT))
        clock = pygame.time.Clock()

        score = 0

        run = True
        while run:
            add_pipe = False
            run = True

            clock.tick(Game.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_ind = 1
            else:
                break

            for bird in birds:
                i = birds.index(bird)
                bird.move()
                ge[i].fitness += .1

                output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
                if output[0] > .5:
                    bird.jump()

            base.move()

            rem = []
            for pipe in pipes:
                pipe.move()

                if pipe.is_off_screen():
                    rem.append(pipe)

                for bird in birds:
                    if pipe.collide(bird):
                        i = birds.index(bird)
                        ge[i].fitness -= 1 # Penalize if the bird collides
                        birds.pop(i)
                        nets.pop(i)
                        ge.pop(i)

                    if pipe.has_passed(bird):
                        add_pipe = True

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5

                pipes.append(Pipe(Game.SPACE_BETWEEN_PIPES))

            for r in rem:
                pipes.remove(r)

            for bird in birds:
                if bird.floor_hit() or bird.touched_sky():
                    i = birds.index(bird)
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

            self.draw_window(win, birds, pipes, base, score, self.GEN)