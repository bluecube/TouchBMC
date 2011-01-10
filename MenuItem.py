import os, pygame
from pygame.locals import *

class MenuItem:
    def __init__(self, image, text, action):
        "Construct the menu item, load its image."
        self.image = pygame.image.load(image).convert_alpha()
        self.text = text
        self.action = action
