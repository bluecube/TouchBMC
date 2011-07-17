#import pygame
import unicodedata
#from pygame.rect import Rect

class Menu:
    """
    A list of menu items.
    Needs Gui initialized!
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the menu, optional keyword arg current sets the index
        of the initially active item.
        """
        self.fill(*args)

        self.last_index = kwargs.get('current', 0)
        self.parent = None
        self.title = ""

    def fill(self, *args):
        """
        Parameters are reference to a parrent menu, followed
        by 3-tuples of image path, item text and item action
        """
        self.items = args
        self.last_index = 0

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

    def __iter__(self):
        return iter(self.items)

    @staticmethod
    def action_helper(menu):
        def action(menuitem, gui):
            gui.set_menu(menu)
        return action

class MenuItem():
    """
    A simple menu item with an image, text and an action.
    Needs Gui initialized!
    """
    def __init__(self, image, text, action):
        "Construct the menu item, load its image."
        self.image = image

        self.text = text
        self.action = action
