#!/usr/bin/python

from xbmc import Xbmc
from clutter_gui import Gui
from menu_impl import MenuImpl
from xbmc_thread import XbmcThread

from config import config

gui = Gui(config)
xbmc = Xbmc(config)
menu = MenuImpl(config, xbmc)
status_updater = XbmcThread(xbmc, gui, config)

gui.set_root_menu(menu.get_root_menu())

status_updater.start()

gui.main()

