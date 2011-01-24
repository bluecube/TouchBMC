import pygame
import unicodedata
from pygame.rect import Rect

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
        self.bar_image = None

    def __len__(self):
        return len(self.items)

    def __getitem__(self, key):
        return self.items[key]

    @staticmethod
    def action_helper(menu):
        def action(gui):
            gui.set_menu(menu)
        return action


class HierarchicalMenu(Menu):
    """
    A menu that splits the items into alphabetical groups.
    """

    # dictionary of pre-rendered letters
    letters = {}

    def __init__(self, config, *args, **kwargs):
        """
        Initialize the menu, config is the configuration dictionary,
        optional keyword arg current sets the index
        of the initially active item.
        """
        self.font = pygame.font.SysFont(config["HierarchicalMenu font"], config["HierarchicalMenu font size"])
        self.FONT_COLOR = config["HierarchicalMenu font color"]
        self.ANTIALIAS = config["antialias"]

        Menu.__init__(self, *args, **kwargs)

    def fill(self, *args):
        """
        Parameters are reference to a parrent menu, followed
        by 3-tuples of image path, item text and item action
        """
        self.submenu = {}
        self.items = []

        self.last_index = 0
        self.bar_image = None

        if len(args) == 0:
            return

        # TODO: Hard coded max length?
        if len(args) < 30:
            Menu.fill(self, *args)
            return

        self.groups = {}
        for item in args:
            self.groups.setdefault(self._get_letter(item.text), []).append(item)

        keys = self.groups.keys()
        keys.sort()

        for key in keys:
            if not HierarchicalMenu.letters.has_key(key):
                HierarchicalMenu.letters[key] = self.font.render(key, self.ANTIALIAS, self.FONT_COLOR)

            def helper(key):
                def action(gui):
                    gui.set_menu(self._get_submenu(key))
                return action

            self.items.append(MenuItem(self.letters[key], "", helper(key)))

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
            self.submenu[key] = Menu(*self.groups[key])

        return self.submenu[key]


class MenuItem():
    """
    A simple menu item with an image, text and an action.
    Needs Gui initialized!
    """
    def __init__(self, image, text, action):
        "Construct the menu item, load its image."
        self.image = image
        self.rect = image.get_rect()

        self.text = text
        self.action = action
