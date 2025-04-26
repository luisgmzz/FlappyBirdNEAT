import pygame
import os

def load_image(name: str):
    return pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", name)))

def rotate_image(img: pygame.Surface, rotation: int, x: int, y: int) :
    rotated_image = pygame.transform.rotate(img, rotation)
    new_rect = rotated_image.get_rect(center=img.get_rect(topleft=(x, y)).center)
    return ( rotated_image, new_rect )