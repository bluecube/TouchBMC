import math
import sys
import pygame
from pygame.locals import *

from menu import Menu
from animation import *
from gui_animations import *
from gui_states import *

class Gui:
    ROW_COUNT = 4
    DIM_TIMER_TICK = 5000
    def __init__(self, config, cache):
        # only initialize what we really need from pygame
        pygame.display.init()
        pygame.font.init()

        pygame.display.set_mode((config["width"], config["height"])) #pygame.NOFRAME, pygame.FULLSCREEN)
        pygame.display.set_caption(config["caption"])
        self._screen = pygame.display.get_surface()

        self._config = config

        self._manager = AnimationManager()
        self._add_animations(config, self._screen, cache)

        self.clock = pygame.time.Clock()
        pygame.time.set_timer(USEREVENT, Gui.DIM_TIMER_TICK)
        
        self.font = pygame.font.SysFont(config["font"], config["font size"])
        self.bg_font = pygame.font.SysFont(config["bg font"], config["bg font size"])

        DimmedState.enter(self)

    def _add_animations(self, config, screen, cache):
        """
        Create and add all animations and images to the animation manager.
        """
        x_6 = self._screen.get_width() // 6
        y_6 = self._screen.get_height() // 6

        self._manager.add(Image(config["background"], 0, 0, cache, True))

        bg_font = pygame.font.SysFont(config["bg font"], config["bg font size"])
        self._bg_text = []
        for i in range(Gui.ROW_COUNT):
            self._bg_text.append(ScrollingText(config, screen, i, bg_font))
            self._manager.add(self._bg_text[i])

        self._foreground_manager = AnimationManager()
        self._manager.add(self._foreground_manager)

        self._position_bar = PositionBar(config, self._screen)
        self._foreground_manager.add(self._position_bar)

        self._scroller = ScrollingMenu(config, screen)
        self._foreground_manager.add(self._scroller)

        self._left = Image(config["left"],  1 * x_6, 3 * y_6, cache)
        self._foreground_manager.add(self._left)

        self._right = Image(config["right"], 5 * x_6, 3 * y_6, cache)
        self._foreground_manager.add(self._right)

        self._back = Image(config["back"],  1 * x_6, 1 * y_6, cache)
        self._foreground_manager.add(self._back)

    def wakeup(self):
        """
        Wake up the gui if it is possibly sleeping in the event loop.
        (works by posting a new event
        """
        pygame.event.post(pygame.event.Event(USEREVENT + 1))

    def set_root_menu(self, menu):
        """
        This is a simplified version of set_menu that doesn't do anything
        like keeping back links and such stuff.
        """
        self._scroller.set_menu(menu)
        self._position_bar.set_menu(menu)

        self._back.disabled = True

        self._manager.update()

    def set_menu(self, menu, is_forward = True):
        """
        Set the current menu to be displayed.
        is_forward should be false when using a back link and true otherwise.
        """

        self._scroller._items.last_index = self._scroller._current

        if is_forward:
            menu.parent = self._scroller._items

            title = self._scroller._items[self._scroller._current].text
            if title:
                menu.title = title
            else:
                # if the current menu item has no title copy the
                # title of the last menu
                menu.title = self._scroller._items.title

        self._back.disabled = not bool(menu.parent)

        print "title is: " + menu.title

        self._scroller.set_menu(menu)
        self._position_bar.set_menu(menu)

        self._arrow_status()

        self._manager.update()

    def go_back(self):
        """
        Move to the parent menu or do nothing if there is no parent.
        """
        if self._scroller._items.parent:
            self.set_menu(self._scroller._items.parent, is_forward = False)

    def action(self):
        """
        Perform the action of the selected menu item.
        """
        self._scroller.stop()

        item = self._scroller._items[self._scroller._current]
        if callable(item.action):
            item.action(item, self)
        else:
            print "Invalid action on item!"

    def scroll_left(self):
        """
        Scroll the menu to the left.
        Returns False if there are no more items, True otherwise.
        """
        ret = self._scroller.start(ScrollingMenu.LEFT)
        self._arrow_status()
        return ret

    def scroll_right(self):
        """
        Scroll the menu to the left.
        Returns False if there are no more items, True otherwise.
        """
        ret = self._scroller.start(ScrollingMenu.RIGHT)
        self._arrow_status()
        return ret

    def _arrow_status(self):
        """
        Show or hide the left and right arrows.
        """
        self._left.disabled = not self._scroller.can_go(ScrollingMenu.LEFT)
        self._right.disabled = not self._scroller.can_go(ScrollingMenu.RIGHT)

    def set_bg_text(self, line_number, text):
        """
        Set the text to be displayed on the background.
        There are four lines available.
        """
        self._bg_text[line_number].set_text(text)

    def can_go(self, direction):
        """
        Find out if the items selection can move in the given direction.
        """
        current = self.current
        if self.anim:
            current += self.anim_direction

        return (direction == self.LEFT and current >= 1) or \
            (direction == self.RIGHT and current < len(self.items) - 1)

    def main(self):
        while True:
            self._work()

    def _work(self):
        """
        Process a single frame. Note: this might block.
        """
        self.clock.tick(self._config["fps"])

        need_ticks = self._manager.update()

        self._manager.draw(self._screen)
        pygame.display.flip()

        for event in pygame.event.get():
            self._process_event(event)

        if not need_ticks:
            # block until the next event if no animation is running
            event = pygame.event.wait();
            self._process_event(event);

    def _process_event(self, event):
        """
        Process a single event
        """

        if event.type == QUIT:
            sys.exit()
        else:
            self._state.handle_event(self, event)
