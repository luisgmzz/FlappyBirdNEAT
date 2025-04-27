import pygame

from game.view.window import Window


class NeatWindow(Window):

    def __init__(self, game):
        super().__init__(game)

        pygame.display.set_caption("NEAT Flappy Bird")


    def draw_window(self):
        score_text = Window.STAT_FONT.render("Score: " + str(self.game.score), 1, Window.COLOR_WHITE)
        gen_text = Window.STAT_FONT.render("Gen: " + str(self.game.gen), 1, Window.COLOR_WHITE)

        self.win.blit(Window.BG_IMG, (0, 0))


        for pipe in self.game.pipes:
            pipe.draw(self.win)

        self.game.base.draw(self.win)

        for bird in self.game.birds:
            bird.draw(self.win)


        self.win.blit(score_text, (Window.WIDTH-10-score_text.get_width(), 10))
        self.win.blit(gen_text, (10, 10))
        pygame.display.update()
