#!/usr/bin/python

import pygame

from config import config
from gui import Gui
from menu import MenuItem, Menu


gui = Gui(config)

root_menu = Menu(None, 
    ("circle.png", "This is a circle", 0),
    ("1.png", "one", 0),
    ("2.png", "two", 0),
    ("3.png", "three", 0),
    ("play.png", "Play", 0),
    ("pause.png", "Pause", 0),
    ("stop.png", "Stop", 0),
)

gui.set_menu(root_menu)

gui.set_bg_text(("Background text", "... with two lines"))

while gui.work():
    pass

