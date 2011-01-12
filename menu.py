import os, pygame
from pygame.locals import *
import unicodedata

class Menu:
    """
    A list of menu items.
    Needs Gui initialized!
    """
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


class HierarchicalMenu(Menu):
    """
    A menu that splits the items into alphabetical groups.
    """

    def __init__(self, config, parent = None, *args):
        self.font = pygame.font.SysFont(config["HierarchicalMenu font"], config["HierarchicalMenu font size"])
        self.FONT_COLOR = config["HierarchicalMenu font color"]
        self.ANTIALIAS = config["antialias"]

        self.fill(parent, *args)

    def fill(self, parent, *args):
        """
        Parameters are reference to a parrent menu, followed
        by 3-tuples of image path, item text and item action
        """
        self.parent = parent
        self.submenu = {}
        self.items = []

        if len(args) == 0:
            return

        self.groups = {};
        for item in args:
            (image, text, action) = item
            self.groups.setdefault(self._get_letter(text), []).append(item)

        keys = self.groups.keys()
        keys.sort()

        for key in keys:
            image = self.font.render(key, self.ANTIALIAS, self.FONT_COLOR)
            def helper(key):
                def action(gui):
                    gui.set_menu(self._get_submenu(key))
                return action

            self.items.append(MenuItem(image, key, helper(key)))

    def _get_letter(self, str):
        """
        Return the letter that will be used to represent the given string.
        """

        # TODO: removing "The", "A", ...

        for c in unicodedata.normalize('NFKD', unicode(str)):
            if c.isalpha():
                return c.upper()
            elif c.isnumeric():
                return "0"

    def _get_submenu(self, key):
        if not self.submenu.has_key(key):
            self.submenu[key] = Menu(self, *self.groups[key])

        return self.submenu[key]


class MenuItem:
    """
    A simple menu item with an image, text and an action.
    Needs Gui initialized!
    """
    def __init__(self, image, text, action):
        "Construct the menu item, load its image."
        if isinstance(image, pygame.Surface):
            self.image = image
        else:
            self.image = pygame.image.load(image).convert_alpha()
        self.text = text
        self.action = action
