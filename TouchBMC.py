#!/usr/bin/python

from image_cache import ImageCache
from xbmc import Xbmc
from gui import Gui
from menu_impl import MenuImpl

from config import config

cache = ImageCache(config)
gui = Gui(config, cache)
xbmc = Xbmc(config)
menu = MenuImpl(config, xbmc, cache)

gui.set_root_menu(menu.get_root_menu())

gui.set_bg_text(0, "In Your Own Sweet Way")
gui.set_bg_text(1, "Robert Balzar Trio")
gui.set_bg_text(2, "Alone (disc 2)")
gui.set_bg_text(3, "05:24 / 05:48")

while True:
    gui.work();

