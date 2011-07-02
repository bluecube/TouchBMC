import threading
import pygame
import datetime
from xbmc import Xbmc
from gui import Gui

class XbmcThread(threading.Thread):
    def __init__(self, xbmc, gui, config):
        threading.Thread.__init__(self)
        self._xbmc = xbmc
        self._gui = gui
        self._config = config
        self._clock = pygame.time.Clock()
        self.daemon = True

    def run(self):
        return
        while True:
            self._clock.tick(self._config["update fps"])
            self._update_status()

    def _update_status(self):
        status = self._xbmc.get_status()

        if not status["playing"]:
            for i in range(Gui.ROW_COUNT):
                self._gui.set_bg_text(i, "")
            return

        rows = self._config["bg text"]
        for i in range(Gui.ROW_COUNT):
            self._gui.set_bg_text(i, rows[i].format(**status))

        self._gui.wakeup()
