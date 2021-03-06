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
        while True:
            self._clock.tick(self._config["update fps"])
            self._update_status()

    def _update_status(self):
        status = self._xbmc.player_status

        if status == Xbmc.IDLE:
            for i in range(Gui.ROW_COUNT):
                self._gui.set_bg_text(i, "")
            return

        labels = self._xbmc.labels
        rows = self._config["bg text"]
        for i in range(Gui.ROW_COUNT):
            self._gui.set_bg_text(i, rows[i].format(**labels))

        self._gui.wakeup()
