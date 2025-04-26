from game.utils import load_image
import pygame
pygame.font.init()

class Window:
    BG_IMG = load_image("bg.png")
    WIDTH = 500
    HEIGHT = 800
    DIMENSIONS = (WIDTH, HEIGHT)

    COLOR_WHITE = (255, 255, 255)
    STAT_FONT = pygame.font.SysFont("comicsans", 50)

    def __init__(self, game):
        self.game = game
        self.win = pygame.display.set_mode(self.DIMENSIONS)

        pygame.display.set_caption("Flappy Bird")

    def draw_window(self):
        text = self.STAT_FONT.render("Score: " + str(self.game.get_score()), 1, self.COLOR_WHITE)

        self.blit(self.BG_IMG, (0, 0))

        self.game.draw_bird()

        self.game.draw_pipes()
        self.game.draw_base()

        self.blit(text, (self.WIDTH-10-text.get_width(), 10))
        pygame.display.update()

    def blit(self, source, dest, area=None, special_flags=0):
        return self.win.blit(source, dest, area, special_flags)
