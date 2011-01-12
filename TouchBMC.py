#!/usr/bin/python

import pygame

from config import config
from gui import Gui
from menu import MenuItem, Menu, HierarchicalMenu

gui = Gui(config)

circle_menu = HierarchicalMenu(config)

root_menu = Menu(None, 
    ("circle.png", "This is a circle", gui.action_helper(circle_menu)),
    ("1.png", "one", 0),
    ("2.png", "two", 0),
    ("3.png", "three", 0),
    ("play.png", "Play", 0),
    ("pause.png", "Pause", 0),
    ("stop.png", "Stop", 0),
)

circle_menu.fill(root_menu,
    ("3.png", "completely", 0),
    ("2.png", "different", 0),
    ("1.png", "menu", 0),
    ("3.png", "abraka", 0),
    ("2.png", "dabra", 0),
    ("1.png", "once", 0),
    ("3.png", "upon", 0),
    ("2.png", "a", 0),
    ("1.png", "midnight", 0),
    ("3.png", "dready", 0),
)

gui.set_menu(root_menu)

gui.set_bg_text(("Background text", "... with two lines"))

while gui.work():
    pass

