#!/usr/bin/python

import pygame
import sys

from config import config
from gui import Gui

gui = Gui(config)

import menu_impl

gui.set_menu(menu_impl.root_menu)

gui.set_bg_text(0, "In Your Own Sweet Way")
gui.set_bg_text(1, "Robert Balzar Trio")
gui.set_bg_text(2, "Alone (disc 2)")
gui.set_bg_text(3, "05:24 / 05:48")

while True:
    gui.work();

