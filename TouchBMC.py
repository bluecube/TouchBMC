#!/usr/bin/python

from image_cache import ImageCache
from xbmc import Xbmc
from gui import Gui
from menu_impl import MenuImpl
from xbmc_thread import XbmcThread

from config import config

cache = ImageCache(config)
gui = Gui(config, cache)
xbmc = Xbmc(config)
menu = MenuImpl(config, xbmc, cache)
status_updater = XbmcThread(xbmc, gui, config)

gui.set_root_menu(menu.get_root_menu())

status_updater.start()

while True:
    gui.work();

