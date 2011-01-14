#!/usr/bin/python

import pygame
import sys

from config import config
from gui import Gui
from menu import MenuItem, Menu, HierarchicalMenu

gui = Gui(config)

circle_menu = HierarchicalMenu(config,
    ("circle.png", "completely", 0),
    ("circle.png", "different", 0),
    ("circle.png", "menu", 0),
    ("circle.png", "abraka", 0),
    ("circle.png", "dabra", 0),
    ("circle.png", "once", 0),
    ("circle.png", "upon", 0),
    ("circle.png", "a", 0),
    ("circle.png", "midnight", 0),
    ("circle.png", "dready", 0),
    ("circle.png", "3, can't you see?", 0),
)

library_menu = Menu(
    ("circle.png", "Artists ...", Menu.action_helper(circle_menu)),
    ("circle.png", "Albums ...", Menu.action_helper(circle_menu)),
    ("circle.png", "Genres ...", Menu.action_helper(circle_menu)),
)

power_menu = Menu(
    ("power.png", "Power off", 0),
    ("close.png", "Exit", lambda gui: sys.exit()),
)

root_menu = Menu(
    ("prev.png", "Previous", 0),
    ("circle.png", "Library ...", Menu.action_helper(library_menu)),
    ("play.png", "Play", 0),
    ("next.png", "Next", 0),
    ("stop.png", "Stop", 0),
    ("power.png", "Power ...", Menu.action_helper(power_menu)),
    current = 2
)

gui.set_menu(root_menu)

gui.set_bg_text(0, "In Your Own Sweet Way")
gui.set_bg_text(1, "Robert Balzar Trio")
gui.set_bg_text(2, "Alone (disc 2)")
gui.set_bg_text(3, "05:24 / 05:48")

while True:
    gui.work();

