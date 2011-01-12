import os, pygame
from pygame.locals import *

class Menu:
    def __init__(self, parent = None, *args):
        """
        Support constructor without params to
        allow forward declarations (breaking up cycles)
        """
        self.fill(parent, *args)

    def fill(self, parent, *args):
        """
        Parameters are reference to a parrent menu, followed
        by 3-tuples of image path, item text and item action
        """
        self.parent = parent
        self.items = map(lambda x: MenuItem(*x), args)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

class MenuItem:
    def __init__(self, image, text, action):
        "Construct the menu item, load its image."
        self.image = pygame.image.load(image).convert_alpha()
        self.text = text
        self.action = action
