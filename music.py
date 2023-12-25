import pygame
from random import uniform


def pin_falling():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('audio/pin_falling.mp3')
        volume = uniform(0.5, 1)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()