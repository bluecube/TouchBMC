#!/usr/bin/python

import pygame

from config import config
from Menu import Menu
from MenuItem import MenuItem

pygame.init()

menu = Menu(config)

menu.set_menu([ \
    MenuItem("circle.png", "This is a circle", 0), \
    MenuItem("1.png", "one", 0), \
    MenuItem("2.png", "two", 0), \
    MenuItem("3.png", "three", 0), \
    MenuItem("play.png", "Play", 0), \
    MenuItem("pause.png", "Pause", 0), \
    MenuItem("stop.png", "Stop", 0), \
])

while menu.work():
    pass

