from bird import Bird
from utils import load_image
import pygame

BG_IMG = load_image("bg.png")
WIN_WIDTH = 500
WIN_HEIGHT = 800

def draw_window(win: pygame.Surface, bird: Bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(200, 200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
    
        draw_window(win, bird)
    pygame.quit()
    quit()

main() 